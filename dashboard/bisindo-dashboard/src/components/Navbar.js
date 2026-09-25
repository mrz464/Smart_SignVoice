import React from 'react';
import {
  AppBar, Toolbar, Typography,
  Button, Box
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" fontWeight="bold" sx={{ flexGrow: 1, color: 'text.primary' }}>
          BicaraUntukku
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button color="primary" onClick={() => navigate('/dashboard')}>Dashboard</Button>
          <Button sx={{ color: 'text.secondary' }} onClick={() => navigate('/students')}>Siswa</Button>
          <Button sx={{ color: 'text.secondary' }} onClick={handleLogout}>Logout</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;