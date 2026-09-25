import React from 'react';
import {
  Box, List, ListItemButton, ListItemIcon,
  ListItemText, Typography, Avatar, Divider
} from '@mui/material';
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import { useNavigate, useLocation } from 'react-router-dom';

export const SIDEBAR_WIDTH = 248;

const menuItems = [
  { label: 'Dashboard', path: '/dashboard', icon: <DashboardRoundedIcon fontSize="small" /> },
  { label: 'Siswa', path: '/students', icon: <GroupRoundedIcon fontSize="small" /> },
];

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <Box
      sx={{
        width: SIDEBAR_WIDTH,
        flexShrink: 0,
        height: '100vh',
        position: 'fixed',
        top: 0,
        left: 0,
        bgcolor: 'background.paper',
        borderRight: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        py: 3,
        px: 2,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, px: 1, mb: 1 }}>
        <Box
          sx={{
            width: 38, height: 38, borderRadius: '10px',
            background: 'linear-gradient(135deg, #38BDF8, #0EA5E9)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 800, color: '#0A1220', fontSize: 16,
          }}
        >
          B
        </Box>
        <Box>
          <Typography variant="subtitle1" sx={{ lineHeight: 1.2 }}>
            BicaraUntukku
          </Typography>
          <Typography variant="caption" color="text.secondary">
            BISINDO Assistant
          </Typography>
        </Box>
      </Box>

      <Typography
        variant="overline"
        color="text.secondary"
        sx={{ px: 1, mt: 4, mb: 1, display: 'block' }}
      >
        Menu
      </Typography>

      <List sx={{ flexGrow: 1 }}>
        {menuItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItemButton
              key={item.path}
              onClick={() => navigate(item.path)}
              selected={active}
              sx={{
                borderRadius: 2,
                mb: 0.5,
                color: active ? 'primary.main' : 'text.secondary',
                '&.Mui-selected': { bgcolor: 'rgba(56,189,248,0.12)' },
                '&.Mui-selected:hover': { bgcolor: 'rgba(56,189,248,0.18)' },
              }}
            >
              <ListItemIcon sx={{ color: active ? 'primary.main' : 'text.secondary', minWidth: 34 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.label}
                primaryTypographyProps={{ fontWeight: active ? 600 : 500, fontSize: 14 }}
              />
            </ListItemButton>
          );
        })}
      </List>

      <Divider sx={{ mb: 1.5 }} />

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, px: 1, mb: 1.5 }}>
        <Avatar sx={{ width: 34, height: 34, bgcolor: 'rgba(56,189,248,0.15)', color: 'primary.main', fontSize: 14, fontWeight: 700 }}>
          G
        </Avatar>
        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
          <Typography variant="body2" fontWeight={600} noWrap>
            Guru Pendamping
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: 'success.main' }} />
            <Typography variant="caption" color="text.secondary">Aktif</Typography>
          </Box>
        </Box>
      </Box>

      <ListItemButton onClick={handleLogout} sx={{ borderRadius: 2, color: 'text.secondary' }}>
        <ListItemIcon sx={{ color: 'text.secondary', minWidth: 34 }}>
          <LogoutRoundedIcon fontSize="small" />
        </ListItemIcon>
        <ListItemText primary="Logout" primaryTypographyProps={{ fontSize: 14, fontWeight: 500 }} />
      </ListItemButton>
    </Box>
  );
}

export default Sidebar;