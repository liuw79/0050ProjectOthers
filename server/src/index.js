import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import materialsRouter from './routes/materials.js';

dotenv.config();

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

app.listen(PORT, () => {
  console.log(`GW.Content 2.0 运行在 http://localhost:${PORT}`);
});
