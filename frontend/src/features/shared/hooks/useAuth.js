import useAuthStore from '../../store/authstore';

export const useAuth = () =>{
    const {user,isAuthenticated, login, logout} = useAuthStore();
    return {user, isAuthenticated, login, logout}
};