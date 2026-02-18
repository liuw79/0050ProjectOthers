import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import materialsRouter from './routes/materials.js';
import coursesRouter from './routes/courses.js';
import topicsRouter from './routes/topics.js';
import suggestMaterialsRouter from './routes/suggest-materials.js';
import writeRouter from './routes/write.js';
import segmentsRouter from './routes/segments.js';

dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// 健康检查
app.get('/health', (req, res) => {
  res.json({ status: 'ok', version: '2.0.0' });
});

// API 路由
app.use('/api/materials', materialsRouter);
app.use('/api/courses', coursesRouter);
app.use('/api/topics', topicsRouter);
app.use('/api/suggest-materials', suggestMaterialsRouter);
app.use('/api/write', writeRouter);
app.use('/api/segments', segmentsRouter);

app.listen(PORT, () => {
  console.log(`GW.Content 2.0 运行在 http://localhost:${PORT}`);
});
