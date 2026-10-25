import {Chip} from '@mui/material';
const colors:Record<string,'default'|'success'|'warning'|'error'|'info'>={LOW:'success',ON_TRACK:'success',COMPLETED:'success',ACCEPTED:'success',NORMAL:'success',MODERATE:'warning',WATCH:'warning',WARNING:'warning',PENDING:'warning',PENDING_REVIEW:'warning',HIGH:'error',CRITICAL:'error',AT_RISK:'error',OVERDUE:'error',REJECTED:'error',OPEN:'info',ACTIVE:'info',IN_PROGRESS:'info'};
export function StatusChip({value}:{value:string}){return <Chip size="small" variant="outlined" color={colors[value]||'default'} label={value.replaceAll('_',' ').toLowerCase().replace(/\b\w/g,c=>c.toUpperCase())}/>}

