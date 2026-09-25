import React, { useState, useEffect } from 'react';
import { Box, Grid, Card, CardContent, Typography, CircularProgress, Alert } from '@mui/material';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts';
import DashboardLayout from '../components/DashboardLayout';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';
import SpellcheckRoundedIcon from '@mui/icons-material/SpellcheckRounded';
import TodayRoundedIcon from '@mui/icons-material/TodayRounded';
import InsightsRoundedIcon from '@mui/icons-material/InsightsRounded';
import { getDashboardStats } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDashboardStats()
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}>
          <CircularProgress />
        </Box>
      </DashboardLayout>
    );
  }

  if (error || !stats) {
    return (
      <DashboardLayout>
        <Alert severity="error">
          Tidak bisa terhubung ke backend. Pastikan server FastAPI sudah berjalan di http://127.0.0.1:8000
        </Alert>
      </DashboardLayout>
    );
  }

  const statsCards = [
    { label: 'Total Siswa', value: stats.total_siswa, trend: 'siswa terdaftar', icon: <GroupRoundedIcon fontSize="small" /> },
    { label: 'Kata Dikuasai', value: stats.kata_dikuasai, trend: `dari ${stats.total_kata} kata`, icon: <SpellcheckRoundedIcon fontSize="small" /> },
    { label: 'Sesi Hari Ini', value: stats.sesi_hari_ini, trend: 'sesi', icon: <TodayRoundedIcon fontSize="small" /> },
    { label: 'Akurasi Rata-rata', value: `${stats.akurasi_rata_rata}%`, trend: 'stabil', icon: <InsightsRoundedIcon fontSize="small" /> },
  ];

  return (
    <DashboardLayout>
      <Typography variant="overline" color="primary.main">Ringkasan</Typography>
      <Typography variant="h5" mb={4}>
        Dashboard overview
      </Typography>

      <Grid container spacing={2.5} mb={4}>
        {statsCards.map((stat, i) => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <Card
              sx={{
                borderRadius: 3, border: '1px solid', borderColor: 'divider', height: '100%',
                '&:hover': { transform: 'translateY(-3px)', borderColor: 'primary.main' },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    width: 40, height: 40, borderRadius: '10px', mb: 2,
                    bgcolor: 'rgba(56,189,248,0.12)', color: 'primary.main',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}
                >
                  {stat.icon}
                </Box>
                <Typography variant="body2" color="text.secondary" mb={0.5}>
                  {stat.label}
                </Typography>
                <Typography variant="h5" mb={0.5}>
                  {stat.value}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {stat.trend}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider', p: 3 }}>
        <Typography variant="overline" color="primary.main">Progres</Typography>
        <Typography variant="h6" mb={3}>
          Perkembangan kosakata per minggu
        </Typography>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={stats.progres_mingguan}>
            <CartesianGrid strokeDasharray="3 3" stroke="#252F48" vertical={false} />
            <XAxis dataKey="minggu" stroke="#8E9BB8" tickLine={false} axisLine={false} />
            <YAxis stroke="#8E9BB8" tickLine={false} axisLine={false} />
            <Tooltip
              cursor={{ fill: 'rgba(56,189,248,0.06)' }}
              contentStyle={{ backgroundColor: '#1A2438', border: '1px solid #252F48', borderRadius: 10 }}
            />
            <Bar dataKey="kata" fill="#38BDF8" radius={[6, 6, 0, 0]} maxBarSize={40} />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </DashboardLayout>
  );
}

export default Dashboard;