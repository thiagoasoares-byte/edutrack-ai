import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { get, post, patch, del } from '../lib/api';

export default function Subjects({ user }) {
  const router = useRouter();
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingSubject, setEditingSubject] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    if (!user) {
      router.replace('/login');
      return;
    }

    // Fetch subjects
    fetchSubjects();
  }, [router, user]);

  const fetchSubjects = async () => {
    try {
      setLoading(true);
      setError(null);

      const subjectsData = await get('subject', '/subjects/list');
      setSubjects(Array.isArray(subjectsData) ? subjectsData : []);
    } catch (err) {
      setError(err.message || 'Failed to load subjects');
      console.error('Error fetching subjects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSubject = async (e) => {
    e.preventDefault();
    try {
      const name = document.getElementById('subject-name').value.trim();
      if (!name) return;

      const newSubject = await post('subject', '/subjects', { name });
      setSubjects([...subjects, newSubject]);

      // Reset form
      document.getElementById('subject-name').value = '';
    } catch (err) {
      setError(err.message || 'Failed to add subject');
      console.error('Error adding subject:', err);
    }
  };

  const handleUpdateSubject = async (e) => {
    e.preventDefault();
    try {
      const name = document.getElementById(`edit-subject-name-${editingSubject.id}`).value.trim();
      if (!name) return;

      const updatedSubject = await patch('subject', `/subjects/${editingSubject.id}`, { name });

      // Update subjects list
      setSubjects(subjects.map(subject =>
        subject.id === editingSubject.id ? updatedSubject : subject
      ));

      // Cancel editing
      setEditingSubject(null);
    } catch (err) {
      setError(err.message || 'Failed to update subject');
      console.error('Error updating subject:', err);
    }
  };

  const handleDeleteSubject = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta disciplina?')) return;

    try {
      await del('subject', `/subjects/${id}`);

      // Remove from subjects list
      setSubjects(subjects.filter(subject => subject.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete subject');
      console.error('Error deleting subject:', err);
    }
  };

  const startEditing = (subject) => {
    setEditingSubject(subject);
  };

  const cancelEditing = () => {
    setEditingSubject(null);
  };

  if (loading) {
    return <div className="flex flex-col items-center justify-center py-12">Loading...</div>;
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border-l-4 border-red-500">
        <h2 className="text-red-800 font-bold mb-2">Error</h2>
        <p className="text-red-700">{error}</p>
        <button
          onClick={fetchSubjects}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-gray-100">
      {/* Header */}
      <header className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-center mb-4">
            📚 Gestão de Disciplinas
          </h1>
        </div>
      </header>

      {/* Add Subject Form */}
      <section className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <form onSubmit={handleAddSubject} className="bg-gray-800 rounded-xl p-6">
            <div className="flex items-center gap-4">
              <input
                type="text"
                id="subject-name"
                placeholder="Nome da disciplina"
                className="flex-1 px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
              />
              <button
                type="submit"
                className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                Adicionar Disciplina
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Subjects List */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {subjects.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-400">
                Nenhuma disciplina cadastrada ainda. Use o formulário acima para adicionar sua primeira disciplina.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {subjects.map((subject) => (
                <div
                  key={subject.id}
                  className="flex items-center justify-between bg-gray-800 rounded-xl p-4 hover:bg-gray-700 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-3 h-3 rounded-full"
                         style={{ backgroundColor: getSubjectColor(subject.id) }}></div>
                    <div>
                      <h3 className="font-semibold text-gray-100">
                        {subject.name}
                      </h3>
                      <p className="text-sm text-gray-500">
                        ID: {subject.id}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    {editingSubject && editingSubject.id === subject.id ? (
                      <>
                        <form onSubmit={handleUpdateSubject} className="flex gap-2">
                          <input
                            type="text"
                            id={`edit-subject-name-${subject.id}`}
                            defaultValue={subject.name}
                            className="px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                          <button
                            type="submit"
                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                          >
                            Salvar
                          </button>
                          <button
                            type="button"
                            onClick={cancelEditing}
                            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500"
                          >
                            Cancelar
                          </button>
                        </form>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => startEditing(subject)}
                          className="px-3 py-1.5 bg-yellow-500 text-white text-xs rounded hover:bg-yellow-600"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleDeleteSubject(subject.id)}
                          className="px-3 py-1.5 bg-red-500 text-white text-xs rounded hover:bg-red-600"
                        >
                          Excluir
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

// Helper function to get subject color
function getSubjectColor(subjectId) {
  if (!subjectId) return '#90A4AE'; // Default gray
  const colors = [
    '#FF8A65',
    '#4DB6AC',
    '#9575CD',
    '#FDD835',
    '#64B5F6',
    '#A1887F',
    '#81C784',
    '#BA68C8',
    '#FFB74D',
    '#90A4AE',
  ];
  return colors[subjectId % colors.length];
}