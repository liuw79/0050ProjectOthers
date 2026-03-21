import os
import json
import re
from typing import Optional

from src.agents.base import Agent
from src.core.feature_list import FeatureListManager
from src.core.git_integrator import GitIntegrator
from src.core.llm.factory import create_llm_client
from src.core.exceptions import LLMError


class InitializerAgent(Agent):
    def __init__(self, config, prompt: Optional[str] = None):
        self.config = config
        self.prompt = prompt
        self._llm_client = None

    @property
    def llm_client(self):
        """Lazy initialization of LLM client."""
        if self._llm_client is None:
            self._llm_client = create_llm_client(
                provider=self.config.llm.provider,
                api_key=self.config.llm.api_key,
                model=self.config.llm.model
            )
        return self._llm_client

    def run(self) -> dict:
        """Run initialization agent."""
        try:
            # 1. Create directories
            self._create_directories()

            # 2. Generate feature list
            self._generate_feature_list()

            # 3. Create init.sh script
            self._create_init_script()

            # 4. Create progress file
            self._create_progress_file()

            # 5. Initialize Git repository
            self._init_git()

            return {
                "status": "success",
                "message": "Initialization complete"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _create_directories(self):
        """Create necessary directories."""
        work_dir = self.config.project.work_dir
        os.makedirs(work_dir, exist_ok=True)

    def _generate_feature_list(self):
        """Generate feature list using LLM or fallback to default."""
        feature_list_path = self.config.project.feature_list_path

        if self.prompt:
            features = self._generate_features_with_llm(self.prompt)
        else:
            # Default example features
            features = [
                {
                    "category": "setup",
                    "description": "Project structure setup",
                    "steps": ["Create directory structure", "Initialize configuration"],
                    "passes": False
                }
            ]

        with open(feature_list_path, 'w') as f:
            json.dump(features, f, indent=2, ensure_ascii=False)

    def _generate_features_with_llm(self, prompt: str) -> list:
        """Use LLM to generate feature list from prompt."""
        system_prompt = """You are a software architect. Given a project description, generate a JSON array of features.

Each feature should have:
- category: one of "setup", "core", "api", "ui", "testing", "docs"
- description: brief description of the feature
- steps: array of implementation steps
- passes: always false (will be updated when implemented)

Return ONLY valid JSON array, no markdown formatting."""

        user_message = f"Generate features for this project:\n\n{prompt}"

        try:
            response = self.llm_client.chat(
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_message}"}
                ],
                max_tokens=self.config.llm.max_tokens
            )

            features = self._parse_feature_response(response)
            return features
        except Exception as e:
            raise LLMError(f"Failed to generate features: {e}")

    def _parse_feature_response(self, response: str) -> list:
        """Parse LLM response into feature list."""
        # Try to extract JSON from response
        json_match = re.search(r'\[[\s\S]*\]', response)
        if json_match:
            try:
                features = json.loads(json_match.group())
                # Validate and normalize features
                normalized = []
                for i, f in enumerate(features):
                    normalized.append({
                        "category": f.get("category", "core"),
                        "description": f.get("description", f"Feature {i+1}"),
                        "steps": f.get("steps", []),
                        "passes": False
                    })
                return normalized
            except json.JSONDecodeError:
                pass

        # Fallback: create single feature from response
        return [{
            "category": "core",
            "description": response[:200] if len(response) > 200 else response,
            "steps": ["Implement as described"],
            "passes": False
        }]

    def _create_init_script(self):
        """Create init.sh script."""
        init_script = self.config.project.init_script
        with open(init_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Development environment initialization\n")
            f.write("echo 'Starting development environment...'\n")
        os.chmod(init_script, 0o755)

    def _create_progress_file(self):
        """Create progress file."""
        progress_file = self.config.project.progress_file
        with open(progress_file, 'w') as f:
            f.write("# Project Progress Log\n")
            f.write("# Initialized\n")

    def _init_git(self):
        """Initialize Git repository."""
        work_dir = self.config.project.work_dir
        integrator = GitIntegrator(work_dir)
        integrator.init_repo()
        integrator.commit("Initial commit", [
            os.path.basename(self.config.project.feature_list_path),
            os.path.basename(self.config.project.progress_file),
            os.path.basename(self.config.project.init_script)
        ])
