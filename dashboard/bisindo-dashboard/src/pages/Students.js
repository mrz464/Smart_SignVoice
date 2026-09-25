import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Avatar, CircularProgress, Alert,
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Chip
} from '@mui/material';
import DashboardLayout from '../components/DashboardLayout';
import { getSessions } from '../services/api';

const initials = (name) => name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();

function Students() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getSessions()
      .then((data) => {
        setStudents(data);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  return (
    <DashboardLayout>
      <Typography variant="overline" color="primary.main">Manajemen</Typography>
      <Typography variant="h5" mb={4}>
        Daftar siswa
      </Typography>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error">
          Tidak bisa terhubung ke backend. Pastikan server FastAPI sudah berjalan di http://127.0.0.1:8000
        </Alert>
      )}

      {!loading && !error && (
        <Card sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
          <CardContent sx={{ p: 0, '&:last-child': { pb: 0 } }}>
            <TableContainer component={Paper} elevation={0} sx={{ backgroundColor: 'transparent' }}>
              <Table>
                <TableHead>
                  <TableRow sx={{ '& th': { borderColor: 'divider', color: 'text.secondary', fontWeight: 600, fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.05em' } }}>
                    <TableCell>Siswa</TableCell>
                    <TableCell>Kata dikuasai</TableCell>
                    <TableCell>Total sesi</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {students.map((s) => (
                    <TableRow key={s.id} hover sx={{ '& td': { borderColor: 'divider' } }}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <Avatar sx={{ width: 32, height: 32, fontSize: 13, bgcolor: 'rgba(56,189,248,0.15)', color: 'primary.main', fontWeight: 700 }}>
                            {initials(s.nama)}
                          </Avatar>
                          <Typography variant="body2" fontWeight={500}>{s.nama}</Typography>
                        </Box>
                      </TableCell>
                      <TableCell sx={{ color: 'text.secondary' }}>{s.kata_dikuasai} kata</TableCell>
                      <TableCell sx={{ color: 'text.secondary' }}>{s.total_sesi} sesi</TableCell>
                      <TableCell>
                        <Chip
                          label={s.status === 'aktif' ? 'Aktif' : 'Tidak Aktif'}
                          color={s.status === 'aktif' ? 'success' : 'error'}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}
    </DashboardLayout>
  );
}

export default Students;