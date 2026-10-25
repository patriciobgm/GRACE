import axios from 'axios';
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:8000/api/v1'});
api.interceptors.request.use(config=>{const token=localStorage.getItem('grace_access');if(token) config.headers.Authorization=`Bearer ${token}`;return config});
api.interceptors.response.use(r=>r,async error=>{const original=error.config;if(error.response?.status===401&&!original._retry&&localStorage.getItem('grace_refresh')){original._retry=true;try{const {data}=await axios.post(`${api.defaults.baseURL}/auth/refresh/`,{refresh:localStorage.getItem('grace_refresh')});localStorage.setItem('grace_access',data.access);original.headers.Authorization=`Bearer ${data.access}`;return api(original)}catch{localStorage.removeItem('grace_access');localStorage.removeItem('grace_refresh');window.location.href='/login'}}return Promise.reject(error)});
export type Page<T>={count:number;next:string|null;previous:string|null;results:T[]};
export const getResults=<T>(data:Page<T>|T[]):T[]=>Array.isArray(data)?data:data.results;

