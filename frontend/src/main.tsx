import React from 'react'; import ReactDOM from 'react-dom/client'; import {BrowserRouter} from 'react-router-dom'; import {QueryClient,QueryClientProvider} from '@tanstack/react-query'; import {CssBaseline,ThemeProvider} from '@mui/material'; import {theme} from './app/theme'; import {AuthProvider} from './auth/AuthContext'; import App from './app/App'; import './app/global.css';
const queryClient=new QueryClient({defaultOptions:{queries:{staleTime:30000,retry:1}}});
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><QueryClientProvider client={queryClient}><ThemeProvider theme={theme}><CssBaseline/><BrowserRouter><AuthProvider><App/></AuthProvider></BrowserRouter></ThemeProvider></QueryClientProvider></React.StrictMode>);

