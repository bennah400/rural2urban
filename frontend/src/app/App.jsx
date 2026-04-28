import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './routes';
import Providers from './providers';

function App() {
  return (
    <Providers>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </Providers>
  );
}

export default App;