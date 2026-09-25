import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#38BDF8',
      light: '#7DD3FC',
      dark: '#0EA5E9',
      contrastText: '#0A1220',
    },
    secondary: { main: '#7DD3FC' },
    background: {
      default: '#10172A',
      paper: '#1A2438',
    },
    text: {
      primary: '#F1F5F9',
      secondary: '#8E9BB8',
    },
    divider: '#252F48',
    success: { main: '#22C55E' },
    error: { main: '#EF4444' },
  },
  shape: { borderRadius: 14 },
  typography: {
    fontFamily: '"Inter", "Segoe UI", sans-serif',
    h4: { fontWeight: 700, letterSpacing: '-0.02em' },
    h5: { fontWeight: 700, letterSpacing: '-0.01em' },
    h6: { fontWeight: 600 },
    subtitle1: { fontWeight: 600 },
    overline: { fontWeight: 700, letterSpacing: '0.12em', fontSize: 11 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          transition: 'transform 0.18s ease, border-color 0.18s ease',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 10 },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600 },
      },
    },
  },
});

export default theme;