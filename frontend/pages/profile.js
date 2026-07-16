import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { updateProfile } from '../lib/api';

export default function Profile({ user }) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updating, setUpdating] = useState(false);
  const [updateError, setUpdateError] = useState(null);
  const [updateSuccess, setUpdateSuccess] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    if (!user) {
      router.replace('/login');
      return;
    }
    setLoading(false);
  }, [router, user]);

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setUpdateError(null);
    setUpdateSuccess(false);
    setUpdating(true);

    try {
      const name = document.getElementById('profile-name').value.trim();
      const email = document.getElementById('profile-email').value.trim();

      if (!name || !email) {
        setUpdateError('Nome e email são obrigatórios');
        return;
      }

      const updatedUser = await updateProfile({ name, email });
      // Update the user context (in a real app, we'd update context or state)
      // For now, we'll just show success message
      setUpdateSuccess(true);

      // Success message disappears after 3 seconds
      setTimeout(() => {
        setUpdateSuccess(false);
      }, 3000);
    } catch (err) {
      setUpdateError(err.message || 'Failed to update profile');
      console.error('Error updating profile:', err);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return <div className="flex flex-col items-center justify-center py-12">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-gray-100">
      {/* Header */}
      <header className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-center mb-4">
            👤 Meu Perfil
          </h1>
        </div>
      </header>

      {/* Profile Form */}
      <section className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gray-800 rounded-xl p-8">
            <form onSubmit={handleUpdateProfile} className="space-y-6">
              <div>
                <label className="block mb-2 text-sm font-medium text-gray-300">Nome completo</label>
                <input
                  type="text"
                  id="profile-name"
                  defaultValue={user.name}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block mb-2 text-sm font-medium text-gray-300">Email</label>
                <input
                  type="email"
                  id="profile-email"
                  defaultValue={user.email}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              {updateError && (
                <div className="p-4 bg-red-50 border-l-4 border-red-500">
                  <p className="text-red-700">{updateError}</p>
                </div>
              )}
              {updateSuccess && (
                <div className="p-4 bg-green-50 border-l-4 border-green-500">
                  <p className="text-green-700">Perfil atualizado com sucesso!</p>
                </div>
              )}
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={updating}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {updating ? 'Atualizando...' : 'Atualizar Perfil'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* User Info Display */}
      <section className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gray-800 rounded-xl p-8">
            <h2 className="text-2xl font-bold mb-4">Informações da Conta</h2>
            <div className="space-y-4 text-left max-w-md mx-auto">
              <div className="flex items-center">
                <span className="flex-shrink-0 text-gray-400">👤</span>
                <span className="ml-3">
                  <span className="font-medium text-gray-300">Nome:</span>
                  <span className="ml-2 text-white">{user.name}</span>
                </span>
              </div>
              <div className="flex items-center">
                <span className="flex-shrink-0 text-gray-400">📧</span>
                <span className="ml-3">
                  <span className="font-medium text-gray-300">Email:</span>
                  <span className="ml-2 text-white">{user.email}</span>
                </span>
              </div>
              <div className="flex items-center">
                <span className="flex-shrink-0 text-gray-400">🆔</span>
                <span className="ml-3">
                  <span className="font-medium text-gray-300">ID:</span>
                  <span className="ml-2 text-white">{user.id}</span>
                </span>
              </div>
              {user.created_at && (
                <div className="flex items-center">
                  <span className="flex-shrink-0 text-gray-400">📅</span>
                  <span className="ml-3">
                    <span className="font-medium text-gray-300">Conta criada em:</span>
                    <span className="ml-2 text-white">{new Date(user.created_at).toLocaleDateString()}</span>
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
          EduTrack AI • Desenvolvido para a Faculdade Impacta
        </div>
      </footer>
    </div>
  );
}