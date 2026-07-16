import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { get, post, patch, del } from '../lib/api';
import { getCurrentUser } from '../lib/auth';
import { format, parseISO, isBefore, differenceInCalendarDays } from 'date-fns';

export default function Tasks({ user }) {
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterSubject, setFilterSubject] = useState('all');

  useEffect(() => {
    // Check if user is logged in
    if (!user) {
      router.replace('/login');
      return;
    }

    // Fetch data
    fetchData();
  }, [router, user]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch subjects
      const subjectsData = await get('subject', '/subjects/list');
      setSubjects(Array.isArray(subjectsData) ? subjectsData : []);

      // Fetch tasks
      const tasksData = await get('academic_tasks', '/academic_tasks/list');
      setTasks(Array.isArray(tasksData) ? tasksData : []);
    } catch (err) {
      setError(err.message || 'Failed to load data');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = tasks.filter(task => {
    // Status filter
    if (filterStatus !== 'all' && task.status !== filterStatus) return false;

    // Subject filter
    if (filterSubject !== 'all' && task.subject_id !== parseInt(filterSubject)) return false;

    return true;
  });

  const handleAddTask = async (e) => {
    e.preventDefault();
    try {
      const title = document.getElementById('task-title').value.trim();
      const description = document.getElementById('task-description').value.trim();
      const subjectId = parseInt(document.getElementById('task-subject').value);
      const dueDate = document.getElementById('task-due-date').value;
      const status = document.getElementById('task-status').value;

      if (!title || !subjectId || !dueDate || !status) return;

      const newTask = await post('academic_tasks', '/academic_tasks', {
        title,
        description,
        subject_id: subjectId,
        due_date: dueDate,
        status
      });

      setTasks([...tasks, newTask]);

      // Reset form
      document.getElementById('task-title').value = '';
      document.getElementById('task-description').value = '';
      document.getElementById('task-subject').value = '';
      document.getElementById('task-due-date').value = '';
      document.getElementById('task-status').value = 'Pendente';
    } catch (err) {
      setError(err.message || 'Failed to add task');
      console.error('Error adding task:', err);
    }
  };

  const handleUpdateTask = async (e) => {
    e.preventDefault();
    try {
      const title = document.getElementById(`edit-task-title-${editingTask.id}`).value.trim();
      const description = document.getElementById(`edit-task-description-${editingTask.id}`).value.trim();
      const subjectId = parseInt(document.getElementById(`edit-task-subject-${editingTask.id}`).value);
      const dueDate = document.getElementById(`edit-task-due-date-${editingTask.id}`).value;
      const status = document.getElementById(`edit-task-status-${editingTask.id}`).value;

      if (!title || !subjectId || !dueDate || !status) return;

      const updatedTask = await patch('academic_tasks', `/academic_tasks/${editingTask.id}`, {
        title,
        description,
        subject_id: subjectId,
        due_date: dueDate,
        status
      });

      // Update tasks list
      setTasks(tasks.map(task =>
        task.id === editingTask.id ? updatedTask : task
      ));

      // Cancel editing
      setEditingTask(null);
    } catch (err) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta tarefa?')) return;

    try {
      await del('academic_tasks', `/academic_tasks/${id}`);

      // Remove from tasks list
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const startEditing = (task) => {
    setEditingTask(task);
  };

  const cancelEditing = () => {
    setEditingTask(null);
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
          onClick={fetchData}
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
            📝 Gestão de Tarefas
          </h1>
        </div>
      </header>

      {/* Filters */}
      <section className="py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gray-800 rounded-xl p-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Status</label>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Todos</option>
                  <option value="Pendente">Pendente</option>
                  <option value="Em andamento">Em andamento</option>
                  <option value="Concluída">Concluída</option>
                </select>
              </div>
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Disciplina</label>
                <select
                  value={filterSubject}
                  onChange={(e) => setFilterSubject(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Todas as disciplinas</option>
                  {subjects.map(subject => (
                    <option key={subject.id} value={subject.id}>
                      {subject.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Add Task Form */}
      <section className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <form onSubmit={handleAddTask} className="bg-gray-800 rounded-xl p-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Título</label>
                <input
                  type="text"
                  id="task-title"
                  placeholder="Digite o título da tarefa"
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Descrição</label>
                <textarea
                  id="task-description"
                  placeholder="Descreva a tarefa (opcional)"
                  rows="3"
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Disciplina</label>
                <select
                  id="task-subject"
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Selecione uma disciplina</option>
                  {subjects.map(subject => (
                    <option key={subject.id} value={subject.id}>
                      {subject.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Data de Vencimento</label>
                <input
                  type="date"
                  id="task-due-date"
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-300">Status</label>
                <select
                  id="task-status"
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Pendente">Pendente</option>
                  <option value="Em andamento">Em andamento</option>
                  <option value="Concluída">Concluída</option>
                </select>
              </div>
            </div>
            <div className="mt-4">
              <button
                type="submit"
                className="w-full px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                Adicionar Tarefa
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Tasks List */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-400">
                Nenhuma tarefa encontrada com os filtros selecionados.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between bg-gray-800 rounded-xl p-4 hover:bg-gray-700 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-3 h-3 rounded-full"
                         style={{ backgroundColor: getSubjectColor(task.subject_id) }}></div>
                    <div>
                      <h3 className="font-semibold text-gray-100">
                        {task.title || 'Sem título'}
                      </h3>
                      <p className="text-sm text-gray-500">
                        📚 {getSubjectName(task.subject_id, subjects)}
                      </p>
                      {task.description && (
                        <p className="text-xs text-gray-600 line-clamp-2">
                          {task.description}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 text-xs rounded-full ${
                          task.status === 'Concluída'
                            ? 'bg-green-500 text-green-900'
                            : task.status === 'Em andamento'
                            ? 'bg-yellow-500 text-yellow-900'
                            : 'bg-red-500 text-red-900'
                        }`}
                      >
                        {task.status}
                      </span>
                      {task.due_date && (
                        <>
                          <span className="text-xs text-gray-400">
                            •
                          </span>
                          <span className="text-xs">
                            {format(parseISO(task.due_date), 'dd/MM/yyyy')}
                          </span>
                        </>
                      )}
                    </div>

                    {editingTask && editingTask.id === task.id ? (
                      <>
                        <form onSubmit={handleUpdateTask} className="flex gap-2">
                          <input
                            type="text"
                            id={`edit-task-title-${task.id}`}
                            defaultValue={task.title}
                            className="px-3 py-1 bg-gray-700 border border-gray-600 rounded-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                          <input
                            type="date"
                            id={`edit-task-due-date-${task.id}`}
                            defaultValue={task.due_date?.split('T')[0]}
                            className="px-3 py-1 bg-gray-700 border border-gray-600 rounded-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                          <select
                            id={`edit-task-status-${task.id}`}
                            defaultValue={task.status}
                            className="px-3 py-1 bg-gray-700 border border-gray-600 rounded-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          >
                            <option value="Pendente">Pendente</option>
                            <option value="Em andamento">Em andamento</option>
                            <option value="Concluída">Concluída</option>
                          </select>
                          <button
                            type="submit"
                            className="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600"
                          >
                            Salvar
                          </button>
                          <button
                            type="button"
                            onClick={cancelEditing}
                            className="px-3 py-1 bg-gray-600 text-white text-xs rounded hover:bg-gray-500"
                          >
                            Cancelar
                          </button>
                        </form>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => startEditing(task)}
                          className="px-2 py-0.5 bg-yellow-500 text-white text-xs rounded hover:bg-yellow-600"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="px-2 py-0.5 bg-red-500 text-white text-xs rounded hover:bg-red-600"
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

// Helper function to get subject name
function getSubjectName(subjectId, subjectsList) {
  if (!subjectId) return 'Sem disciplina';
  const subject = subjectsList.find(s => s.id === subjectId);
  return subject ? subject.name : `Matéria #${subjectId}`;
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