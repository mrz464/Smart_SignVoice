import React from 'react';
import { Box } from '@mui/material';
import Sidebar, { SIDEBAR_WIDTH } from './Sidebar';

function DashboardLayout({ children }) {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box sx={{ flexGrow: 1, ml: `${SIDEBAR_WIDTH}px`, p: 4 }}>
        {children}
      </Box>
    </Box>
  );
}

export default DashboardLayout;