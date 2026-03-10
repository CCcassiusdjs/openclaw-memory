import { useState, useEffect } from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'
import axios from 'axios'

const queryClient = new QueryClient()

// Types
interface User {
  id: string
  username: string
  email: string
  role: string
  last_login?: string
}

interface AuthResponse {
  access_token: string
  token_type: string
}

// API
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Login Component
function Login({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    
    try {
      const res = await api.post<AuthResponse>('/auth/login', { username, password })
      localStorage.setItem('token', res.data.access_token)
      onLogin()
    } catch {
      setError('Credenciais inválidas')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">🦾 LSA Lab Platform</h1>
        <p className="login-subtitle">Gerenciamento Centralizado do Laboratório</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Usuário</label>
            <input
              type="text"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Digite seu usuário"
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Senha</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Digite sua senha"
              required
            />
          </div>
          
          {error && <p style={{ color: 'var(--error)', marginBottom: '16px' }}>{error}</p>}
          
          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        
        <p style={{ marginTop: '24px', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '14px' }}>
          Demo: admin / lsa@dm1n
        </p>
      </div>
    </div>
  )
}

// Dashboard Widget Components
function ClusterStatusWidget() {
  const [nodes, setNodes] = useState<any[]>([])
  const [services, setServices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [nodesRes, servicesRes] = await Promise.all([
          api.get('/cluster/nodes'),
          api.get('/cluster/services')
        ])
        setNodes(nodesRes.data)
        setServices(servicesRes.data)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="widget-content">Carregando...</div>

  return (
    <div className="widget-content">
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '12px' }}>Nodes ({nodes.length})</h4>
        {nodes.map((node: any) => (
          <div key={node.hostname} style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
            <span className={`status-badge ${node.status === 'Ready' ? 'status-running' : 'status-stopped'}`}>
              {node.status}
            </span>
            <span>{node.hostname}</span>
            <span style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>({node.role})</span>
          </div>
        ))}
      </div>
      
      <div>
        <h4 style={{ marginBottom: '12px' }}>Serviços ({services.length})</h4>
        <div style={{ maxHeight: '200px', overflow: 'auto' }}>
          {services.map((svc: any) => (
            <div key={svc.name} style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <span className={`status-badge ${svc.replicas === '1/1' ? 'status-running' : 'status-stopped'}`}>
                {svc.replicas}
              </span>
              <span style={{ fontSize: '13px' }}>{svc.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function MetricsWidget() {
  const [metrics, setMetrics] = useState<any>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await api.get('/cluster/metrics')
        setMetrics(res.data)
      } finally {
        setLoading(false)
      }
    }
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="widget-content">Carregando...</div>

  return (
    <div className="widget-content">
      <div className="metrics-grid">
        {Object.entries(metrics.nodes || {}).map(([name, data]: [string, any]) => (
          <div key={name} className="metric-card">
            <div className="metric-label">{name}</div>
            <div style={{ marginTop: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '12px' }}>CPU</span>
                <span style={{ fontSize: '12px', fontWeight: '600' }}>{data.cpu}%</span>
              </div>
              <div style={{ height: '4px', background: 'var(--surface-light)', borderRadius: '2px' }}>
                <div style={{ width: `${data.cpu}%`, height: '100%', background: 'var(--primary)', borderRadius: '2px' }} />
              </div>
            </div>
            <div style={{ marginTop: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '12px' }}>RAM</span>
                <span style={{ fontSize: '12px', fontWeight: '600' }}>{data.memory}%</span>
              </div>
              <div style={{ height: '4px', background: 'var(--surface-light)', borderRadius: '2px' }}>
                <div style={{ width: `${data.memory}%`, height: '100%', background: 'var(--success)', borderRadius: '2px' }} />
              </div>
            </div>
          </div>
        ))}
      </div>
      <div style={{ marginTop: '16px', display: 'flex', gap: '16px', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div className="metric-value">{metrics.total_containers}</div>
          <div className="metric-label">Containers</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div className="metric-value" style={{ color: 'var(--success)' }}>{metrics.running_containers}</div>
          <div className="metric-label">Running</div>
        </div>
      </div>
    </div>
  )
}

function DoorControlWidget() {
  const [status, setStatus] = useState<any>({})
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await api.get('/door/status')
        setStatus(res.data)
      } catch {}
    }
    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleOpen = async () => {
    setLoading(true)
    try {
      await api.post('/door/open')
      setStatus((s: any) => ({ ...s, status: 'open' }))
    } finally {
      setLoading(false)
    }
  }

  const handleClose = async () => {
    setLoading(true)
    try {
      await api.post('/door/close')
      setStatus((s: any) => ({ ...s, status: 'closed' }))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="door-control">
      <div className="door-status" style={{ fontSize: '64px' }}>
        {status.status === 'open' ? '🚪' : '🚪'}
      </div>
      <span className={`status-badge ${status.status === 'open' ? 'status-stopped' : 'status-running'}`}>
        {status.status === 'open' ? 'ABERTA' : 'FECHADA'}
      </span>
      {status.lockout_remaining > 0 && (
        <p style={{ color: 'var(--warning)' }}>Lockout: {status.lockout_remaining}s</p>
      )}
      <div style={{ display: 'flex', gap: '16px', marginTop: '16px' }}>
        <button
          className="btn btn-primary"
          onClick={handleOpen}
          disabled={loading || status.status === 'open'}
        >
          {loading ? '...' : 'Abrir'}
        </button>
        <button
          className="btn btn-secondary"
          onClick={handleClose}
          disabled={loading || status.status === 'closed'}
        >
          {loading ? '...' : 'Fechar'}
        </button>
      </div>
      <p style={{ marginTop: '16px', color: 'var(--text-secondary)', fontSize: '12px' }}>
        Última ação: {status.last_action || '-'} por {status.last_user || '-'}
      </p>
    </div>
  )
}

// Main Dashboard
function Dashboard() {
  return (
    <div className="page-content">
      <h1 style={{ marginBottom: '24px' }}>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div>
          <div className="widget-card" style={{ marginBottom: '20px' }}>
            <div className="widget-header">
              <h3 className="widget-title">📊 Status do Cluster</h3>
            </div>
            <ClusterStatusWidget />
          </div>
          
          <div className="widget-card">
            <div className="widget-header">
              <h3 className="widget-title">📈 Métricas</h3>
            </div>
            <MetricsWidget />
          </div>
        </div>
        
        <div>
          <div className="widget-card">
            <div className="widget-header">
              <h3 className="widget-title">🚪 Controle de Acesso</h3>
            </div>
            <DoorControlWidget />
          </div>
        </div>
      </div>
    </div>
  )
}

// Services Page
function Services() {
  const [services, setServices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/cluster/services').then(res => {
      setServices(res.data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="page-content">
      <h1 style={{ marginBottom: '24px' }}>Serviços</h1>
      
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          {services.map((svc: any) => (
            <div key={svc.name} className="widget-card">
              <div className="widget-header">
                <h4>{svc.name}</h4>
                <span className={`status-badge ${svc.replicas === '1/1' ? 'status-running' : 'status-stopped'}`}>
                  {svc.replicas}
                </span>
              </div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>{svc.image}</p>
              {svc.ports && svc.ports.length > 0 && (
                <p style={{ marginTop: '8px', fontSize: '12px' }}>
                  Portas: {svc.ports.join(', ')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// Users Page (Admin)
function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/users').then(res => {
      setUsers(res.data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="page-content">
      <h1 style={{ marginBottom: '24px' }}>Usuários</h1>
      
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <div className="widget-card">
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)' }}>
                <th style={{ textAlign: 'left', padding: '12px' }}>Usuário</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Email</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Role</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Último Login</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user: User) => (
                <tr key={user.id} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '12px' }}>{user.username}</td>
                  <td style={{ padding: '12px' }}>{user.email}</td>
                  <td style={{ padding: '12px' }}>
                    <span className={`status-badge ${user.role === 'sudo' ? 'status-running' : 'status-stopped'}`}>
                      {user.role}
                    </span>
                  </td>
                  <td style={{ padding: '12px', color: 'var(--text-secondary)' }}>
                    {user.last_login || 'Nunca'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// Main Layout
function Layout({ children, user, onLogout, currentPage, setCurrentPage }: { 
  children: React.ReactNode; 
  user: User; 
  onLogout: () => void;
  currentPage: string;
  setCurrentPage: (page: string) => void;
}) {

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'services', label: 'Serviços', icon: '🔧' },
    { id: 'terminal', label: 'Terminal', icon: '💻' },
    ...(user.role === 'sudo' ? [{ id: 'users', label: 'Usuários', icon: '👥' }] : []),
    { id: 'settings', label: 'Configurações', icon: '⚙️' }
  ]

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">🦾 LSA Lab</div>
        </div>
        
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <div
              key={item.id}
              className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => setCurrentPage(item.id)}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </div>
          ))}
        </nav>
        
        <div className="sidebar-footer">
          <div className="user-menu" onClick={onLogout}>
            <div className="user-avatar">{user.username[0].toUpperCase()}</div>
            <div className="user-info">
              <div className="user-name">{user.username}</div>
              <div className="user-role">{user.role}</div>
            </div>
          </div>
        </div>
      </aside>
      
      <main className="main-content">
        <header className="header">
          <h2 style={{ fontSize: '20px', fontWeight: '600' }}>
            {navItems.find(i => i.id === currentPage)?.label || 'Dashboard'}
          </h2>
          <div style={{ display: 'flex', gap: '12px' }}>
            <span className="status-badge status-running">Online</span>
          </div>
        </header>
        
        {children}
      </main>
    </div>
  )
}

// App
function App() {
  const [user, setUser] = useState<User | null>(null)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      api.get('/auth/me')
        .then(res => setUser(res.data))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const handleLogin = async () => {
    const res = await api.get('/auth/me')
    setUser(res.data)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  if (loading) {
    return <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      Carregando...
    </div>
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'services':
        return <Services />
      case 'users':
        return user.role === 'sudo' ? <Users /> : <Dashboard />
      case 'terminal':
        return (
          <div className="page-content">
            <h1 style={{ marginBottom: '24px' }}>Terminal</h1>
            <div className="widget-card">
              <div className="terminal-container">
                <div style={{ padding: '20px', color: 'var(--text-secondary)', textAlign: 'center' }}>
                  Terminal Web - Em desenvolvimento
                </div>
              </div>
            </div>
          </div>
        )
      case 'settings':
        return (
          <div className="page-content">
            <h1 style={{ marginBottom: '24px' }}>Configurações</h1>
            <div className="widget-card">
              <p>Configurações do usuário e preferências de dashboard.</p>
            </div>
          </div>
        )
      default:
        return <Dashboard />
    }
  }

  return (
    <QueryClientProvider client={queryClient}>
      <Layout user={user} onLogout={handleLogout} currentPage={currentPage} setCurrentPage={setCurrentPage}>
        {renderPage()}
      </Layout>
    </QueryClientProvider>
  )
}

export default App