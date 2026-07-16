import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { get } from '../lib/api';
import { getCurrentUser } from '../lib/auth';
import { format, parseISO, differenceInCalendarDays, startOfWeek, endOfWeek, startOfMonth, endOfMonth } from 'date-fns';

export default function Reports({ user }) {
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  // Calculate statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.status === 'Concluída').length;
  const pendingTasks = tasks.filter(task => task.status === 'Pendente').length;
  const inProgressTasks = tasks.filter(task => task.status === 'Em andamento').length;
  const overdueTasks = tasks.filter(task =>
    task.status !== 'Concluída' &&
    task.due_date &&
    isBefore(parseISO(task.due_date.split('T')[0]), new Date())
  ).length;

  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Tasks completed this week
  const startOfThisWeek = startOfWeek(new Date());
  const endOfThisWeek = endOfWeek(new Date());
  const completedThisWeek = tasks.filter(task => {
    if (task.status !== 'Concluída') return false;
    if (!task.updated_at) return false;
    const updatedAt = new Date(task.updated_at);
    return !isBefore(updatedAt, startOfThisWeek) && !isAfter(updatedAt, endOfThisWeek);
  }).length;

  // Tasks completed this month
  const startOfThisMonth = startOfMonth(new Date());
  const endOfThisMonth = endOfMonth(new Date());
  const completedThisMonth = tasks.filter(task => {
    if (task.status !== 'Concluída') return false;
    if (!task.updated_at) return false;
    const updatedAt = new Date(task.updated_at);
    return !isBefore(updatedAt, startOfThisMonth) && !isAfter(updatedAt, endOfThisMonth);
  }).length;

  // Tasks by subject
  const tasksBySubject = subjects.map(subject => {
    const count = tasks.filter(task => task.subject_id === subject.id).length;
    const completed = tasks.filter(task => task.subject_id === subject.id && task.status === 'Concluída').length;
    return {
      subject: subject.name,
      total: count,
      completed: completed,
      percentage: count > 0 ? Math.round((completed / count) * 100) : 0
    };
  });

  // Tasks due soon (next 7 days)
  const sevenDaysFromNow = new Date();
  sevenDaysFromNow.setDate(sevenDaysFromNow.getDate() + 7);
  const dueSoon = tasks.filter(task =>
    task.status !== 'Concluída' &&
    task.due_date &&
    !isBefore(parseISO(task.due_date.split('T')[0]), new Date()) &&
    isBefore(parseISO(task.due_date.split('T')[0]), sevenDaysFromNow)
  ).sort((a, b) => {
    const dateA = new Date(a.due_date);
    const dateB = new Date(b.due_date);
    return dateA - dateB;
  });

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
            📊 Relatórios e Estatísticas
          </h1>
        </div>
      </header>

      {/* Overview Stats */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {/* Total Tasks */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">📝</span> Total de Tarefas
              </h3>
              <p className="text-4xl font-bold text-blue-400">{totalTasks}</p>
            </div>

            {/* Completed Tasks */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">✅</span> Tarefas Concluídas
              </h3>
              <p className="text-4xl font-bold text-green-400">{completedTasks}</p>
            </div>

            {/* Pending Tasks */}
            <div className="bg-gray-800 rounded-xl p-6>
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">⏳</span> Tarefas Pendentes
              </h3>
              <p className="text-4xl font-bold text-yellow-400">{pendingTasks}</p>
            </div>

            {/* Completion Rate */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">📊</span> Taxa de Conclusão
              </h3>
              <p className="text-4xl font-bold text-purple-400">{completionRate}%</p>
            </div>
          </div>
        </div>
      </section>

      {/* Progress Sections */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-8">
            {/* Weekly Progress */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-4">📅 Progresso Semanal</h2>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-400">Tarefas concluídas nesta semana:</span>
                  <span className="font-bold text-white">{completedThisWeek}</span>
                </div>
                <div className="bg-gray-700 rounded-full h-4">
                  <div
                    className={`bg-gradient-to-r from-blue-400 to-indigo-400 h-full rounded-full transition-all duration-500`}
                    style={{ width: `${Math.min(completedThisWeek * 10, 100)}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-400 mt-1">
                  Meta: 10 tarefas por semana
                </p>
              </div>
            </div>

            {/* Monthly Progress */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-4">📆 Progresso Mensal</h2>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-400">Tarefas concluídas neste mês:</span>
                  <span className="font-bold text-white">{completedThisMonth}</span>
                </div>
                <div className="bg-gray-700 rounded-full h-4">
                  <div
                    className={`bg-gradient-to-r from-green-400 to-teal-400 h-full rounded-full transition-all duration-500`}
                    style={{ width: `${Math.min(completedThisMonth * 5, 100)}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-400 mt-1">
                  Meta: 50 tarefas por mês
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tasks by Subject */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold mb-6 text-center">📚 Desempenho por Disciplina</h2>
          <div className="space-y-4">
            {tasksBySubject.map((subjectStat, index) => (
              <div key={index} className="bg-gray-800 rounded-xl p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-100">{subjectStat.subject}</h3>
                    <p className="text-sm text-gray-400">
                      {subjectStat.completed} de {subjectStat.total} tarefas concluídas
                    </p>
                  </div>
                  <div className="w-full mt-2">
                    <div className="bg-gray-700 rounded-full h-2.5">
                      <div
                        className={`bg-gradient-to-r from-${getSubjectColorIndex(index)}-400 to-${getSubjectColorIndex(index)}-500 h-full rounded-full transition-all duration-500`}
                        style={{ width: `${subjectStat.percentage}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-400 mt-1 text-right">
                      {subjectStat.percentage}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Upcoming Deadlines */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold mb-6 text-center">⏰ Próximos Vencimentos (Próximos 7 dias)</h2>
          {dueSoon.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-green-400">
                ✅ Nenhuma tarefa vencendo nos próximos 7 dias!
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {dueSoon.map((task, index) => (
                <div key={index} className="bg-gray-800 rounded-xl p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-100">
                        {task.title || 'Sem título'}
                      </h3>
                      <p className="text-sm text-gray-400">
                        📚 {getSubjectName(task.subject_id, subjects)}
                      </p>
                      {task.description && (
                        <p className="text-xs text-gray-600 line-clamp-2 mt-1">
                          {task.description}
                        </p>
                      )}
                    </div>
                    <div className="text-right">
                      <span
                        className={`px-2 py-0.5 text-xs rounded-full ${
                          isBefore(parseISO(task.due_date.split('T')[0]), new Date())
                            ? 'bg-red-500 text-red-900'
                            : 'bg-yellow-500 text-yellow-900'
                        }`}
                      >
                        {Math.abs(differenceInCalendarDays(parseISO(task.due_date.split('T')[0]), new Date()))}d
                      </span>
                      <p className="mt-1 text-xs text-gray-400">
                        {format(parseISO(task.due_date), 'dd/MM/yyyy')}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
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

// Helper function to get subject name
function getSubjectName(subjectId, subjectsList) {
  if (!subjectId) return 'Sem disciplina';
  const subject = subjectsList.find(s => s.id === subjectId);
  return subject ? subject.name : `Matéria #${subjectId}`;
}

// Helper function to get color index for subjects
function getSubjectColorIndex(index) {
  const colors = ['blue', 'green', 'yellow', 'red', 'purple', 'indigo', 'pink', 'teal'];
  return colors[index % colors.length];
}

// Helper function to check if date is after another date
function isAfter(dateA, dateB) {
  return dateA > dateB;
}