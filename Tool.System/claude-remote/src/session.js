/**
 * 会话管理模块
 */

import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 项目根目录
const PROJECTS_ROOT = '/Users/comdir/SynologyDrive/0050Project';

// 加载项目配置
const projectsPath = join(__dirname, '../config/projects.json');
let projectsConfig = JSON.parse(readFileSync(projectsPath, 'utf-8'));

// 动态项目缓存
const dynamicProjects = {};

// 会话状态
const statePath = join(__dirname, '../config/session.json');

let state = {
  currentProject: 'sys',
  currentPath: null,
  history: []
};

// 加载持久化状态
if (existsSync(statePath)) {
  try {
    state = JSON.parse(readFileSync(statePath, 'utf-8'));
  } catch (e) {
    console.log('无法加载会话状态，使用默认值');
  }
}

export function saveState() {
  writeFileSync(statePath, JSON.stringify(state, null, 2));
}

export function getCurrentProject() {
  return state.currentProject;
}

// 获取所有可用目录（扫描0050Project）
function getAvailableDirectories() {
  const dirs = {};
  try {
    const entries = readdirSync(PROJECTS_ROOT);
    for (const entry of entries) {
      const fullPath = join(PROJECTS_ROOT, entry);
      try {
        if (statSync(fullPath).isDirectory() && !entry.startsWith('.')) {
          dirs[entry] = {
            name: entry,
            path: fullPath,
            description: '动态目录'
          };
        }
      } catch (e) {
        // 忽略无权限的目录
      }
    }
  } catch (e) {
    console.error('扫描目录失败:', e);
  }
  return dirs;
}

// 查找项目（支持预定义和动态目录）
function findProject(projectKey) {
  // 1. 先查预定义项目
  if (projectsConfig.projects[projectKey]) {
    return projectsConfig.projects[projectKey];
  }

  // 2. 再查动态缓存
  if (dynamicProjects[projectKey]) {
    return dynamicProjects[projectKey];
  }

  // 3. 直接匹配目录名
  const directPath = join(PROJECTS_ROOT, projectKey);
  if (existsSync(directPath) && statSync(directPath).isDirectory()) {
    const project = {
      name: projectKey,
      path: directPath,
      description: '动态目录'
    };
    dynamicProjects[projectKey] = project;
    return project;
  }

  // 4. 模糊匹配（部分名称）
  const allDirs = getAvailableDirectories();
  const matches = Object.keys(allDirs).filter(name =>
    name.toLowerCase().includes(projectKey.toLowerCase()) ||
    projectKey.toLowerCase().includes(name.toLowerCase())
  );

  if (matches.length === 1) {
    const project = allDirs[matches[0]];
    dynamicProjects[projectKey] = project;
    return project;
  }

  if (matches.length > 1) {
    return { error: `找到多个匹配: ${matches.join(', ')}`, matches };
  }

  return null;
}

export function setCurrentProject(projectKey) {
  const project = findProject(projectKey);

  if (!project) {
    // 列出可用目录提示
    const dirs = Object.keys(getAvailableDirectories());
    const suggestions = dirs.slice(0, 10).join(', ');
    return {
      success: false,
      error: `未知项目: ${projectKey}`,
      hint: `可用目录: ${suggestions}${dirs.length > 10 ? '...' : ''}`
    };
  }

  if (project.error) {
    return { success: false, error: project.error, matches: project.matches };
  }

  state.currentProject = projectKey;
  state.currentPath = project.path;
  saveState();
  return { success: true, project };
}

export function getProject(projectKey) {
  const project = findProject(projectKey);
  return project && !project.error ? project : null;
}

export function getCurrentProjectInfo() {
  // 优先使用当前路径
  if (state.currentPath) {
    return {
      name: state.currentProject,
      path: state.currentPath,
      description: '当前目录'
    };
  }
  // 再查预定义项目
  if (projectsConfig.projects[state.currentProject]) {
    return projectsConfig.projects[state.currentProject];
  }
  // 返回基本信息
  return {
    name: state.currentProject || '未知',
    path: state.currentPath || '未知',
    description: '当前项目'
  };
}

export function getAllProjects() {
  // 合并预定义项目和动态扫描的目录
  const allDirs = getAvailableDirectories();
  return { ...allDirs, ...projectsConfig.projects };
}

export function addHistory(role, content, project = null) {
  state.history.push({
    role,
    content,
    project: project || state.currentProject,
    timestamp: new Date().toISOString()
  });

  // 只保留最近 100 条
  if (state.history.length > 100) {
    state.history = state.history.slice(-100);
  }

  saveState();
}

export function getHistory(count = 20, project = null) {
  let history = state.history;

  if (project) {
    history = history.filter(h => h.project === project);
  }

  return history.slice(-count);
}
