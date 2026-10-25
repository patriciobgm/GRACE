import {Alert,Box,CircularProgress,Typography} from '@mui/material';
export const Loading=()=> <Box sx={{p:5,textAlign:'center'}}><CircularProgress size={28}/><Typography sx={{mt:1}}>Loading GRACE data…</Typography></Box>;
export const ErrorState=({message='Unable to load this GRACE record.'}:{message?:string})=><Alert severity="error">{message}</Alert>;
export const EmptyState=({message}:{message:string})=><Box sx={{p:5,textAlign:'center',border:'1px dashed #c7d0d9',bgcolor:'#fafbfc'}}><Typography color="text.secondary">{message}</Typography></Box>;

