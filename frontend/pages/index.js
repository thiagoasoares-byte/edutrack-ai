import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { get } from '../lib/api';
import { format, subDays, isBefore, parseISO, differenceInCalendarDays } from 'date-fns';

export default function Home({ user }) {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [tasks, setTasks] = useState([]);
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

  // Calculate metrics
  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];

  const totalSubjects = subjects.length;
  const totalTasks = tasks.length;

  const pendingTasks = tasks.filter(
    (task) =>
      task.status !== 'Concluída' &&
      (task.status === 'Pendente' || task.status === 'Em andamento')
  ).length;

  const overdueTasks = tasks.filter(
    (task) =>
      task.status !== 'Concluída' &&
      task.due_date &&
      isBefore(parseISO(task.due_date.split('T')[0]), today)
  ).length;

  const completedTasks = tasks.filter(
    (task) => task.status === 'Concluída'
  ).length;

  const progressPct =
    totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Get upcoming tasks (not completed and due today or in future)
  const upcomingTasks = tasks
    .filter(
      (task) =>
        task.status !== 'Concluída' &&
        task.due_date &&
        !isBefore(parseISO(task.due_date.split('T')[0]), today)
    )
    .sort((a, b) => {
      const dateA = new Date(a.due_date);
      const dateB = new Date(b.due_date);
      return dateA - dateB;
    })
    .slice(0, 5);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-gray-100">
      {/* Header */}
      <header className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-center">
            👋 Olá, {user?.name || 'Aluno'}!
          </h1>
          <p className="mt-2 text-center text-gray-400">
            Aqui está um resumo do seu progresso acadêmico.
          </p>
        </div>
      </header>

      {/* Metrics */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {/* Subjects */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">📚</span> Disciplinas
              </h3>
              <p className="text-4xl font-bold text-blue-400">
                {totalSubjects}
              </p>
            </div>

            {/* Pending Tasks */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">📝</span> Tarefas Pendentes
              </h3>
              <p className="text-4xl font-bold text-yellow-400">
                {pendingTasks}
              </p>
            </div>

            {/* Overdue Tasks */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">⚠️</span> Em Atraso
              </h3>
              <p className="text-4xl font-bold text-red-400">
                {overdueTasks}
              </p>
              {overdueTasks > 0 && (
                <p className="mt-1 text-sm text-red-300">
                  -{overdueTasks}
                </p>
              )}
            </div>

            {/* Progress */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">✅</span> Progresso Geral
              </h3>
              <div className="flex items-baseline">
                <p className="text-4xl font-bold text-green-400 mr-2">
                  {progressPct}%
                </p>
                <p className="text-sm text-gray-400">
                  {completedTasks} de {totalTasks} tarefas concluídas
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Progress Bar */}
      <section className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold mb-4">📊 Progresso das Tarefas</h2>
          <div className="bg-gray-700 rounded-full h-4">
            <div
              className={`bg-gradient-to-r from-green-400 to-teal-400 h-full rounded-full transition-all duration-500 ${
                progressPct === 100 ? 'animate-pulse' : ''
              }`}
              style={{ width: `${progressPct}%` }}
            ></div>
          </div>
          <p className="mt-2 text-center text-sm text-gray-400">
            {completedTasks} de {totalTasks} tarefas concluídas
          </p>
        </div>
      </section>

      {/* Upcoming Tasks */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-xl font-bold mb-6">⏰ Próximas Tarefas</h2>

          {upcomingTasks.length === 0 && (
            <div className="text-center py-8">
              {totalTasks === 0 ? (
                <>
                  <p className="text-gray-400">
                    🎉 Nenhuma tarefa cadastrada ainda. Acesse
                    <a href="/tarefas" className="text-blue-400 underline">
                      Tarefas</a
                    > no menu lateral para começar!
                  </p>
                </>
              ) : (
                <p className="text-green-400">
                  ✅ Não há tarefas pendentes com prazo futuro.
                </p>
              )}
            </div>
          )}

          {upcomingTasks.length > 0 && (
            <div className="space-y-4">
              {upcomingTasks.map((task) => {
                const dueDate = parseISO(task.due_date.split('T')[0]);
                const daysLeft = differenceInCalendarDays(dueDate, today);
                const isOverdue = daysLeft < 0;
                const isDueToday = daysLeft === 0;
                const isDueSoon = daysLeft > 0 && daysLeft <= 3;

                // Determine badge color
                let bgColor = 'bg-gray-600';
                let textColor = 'text-gray-200';
                if (isDueToday) {
                  bgColor = 'bg-yellow-500';
                  textColor = 'text-yellow-900';
                } else if (isDueSoon) {
                  bgColor = 'bg-orange-500';
                  textColor = 'text-orange-900';
                } else if (daysLeft > 3) {
                  bgColor = 'bg-green-500';
                  textColor = 'text-green-900';
                }

                // Get subject name
                const subject = subjects.find(
                  (s) => s.id === task.subject_id
                );
                const subjectName = subject
                  ? subject.name
                  : task.subject_id
                  ? `Matéria #${task.subject_id}`
                  : '—';

                return (
                  <div
                    key={task.id}
                    className="flex items-center bg-gray-800 rounded-xl p-4 hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex-shrink-0 w-3 h-3 rounded-full"
                         style={{ backgroundColor: getSubjectColor(subject.id) }}></div>
                    <div className="flex-1 ml-4">
                      <div className="flex justify-between items-start">
                        <h3 className="font-semibold text-gray-100">
                          {task.title || 'Sem título'}
                        </h3>
                        <span
                          className={`px-2 py-0.5 text-xs rounded-full ${bgColor} ${textColor}`}
                        >
                          {isDueToday
                            ? 'Hoje'
                            : isOverdue
                            ? `Atrasado ${Math.abs(daysLeft)}d`
                            : `${daysLeft}d`}
                        </span>
                      </div>
                      <p className="mt-1 text-truncate max-w-xs text-gray-400">
                        📚 {subjectName}
                      </p>
                      {task.description && (
                        <p className="mt-1 text-xs text-gray-500 line-clamp-2">
                          {task.description}
                        </p>
                      )}
                    </div>
                    <div className="flex-shrink-0 text-right">
                      <p className="text-xs text-gray-400">
                        {task.due_date?.split('T')[0] || '—'}
                      </p>
                      <span
                        className={`inline-flex items-center px-2 py-0.5 text-xs rounded-full ${
                          task.status === 'Concluída'
                            ? 'bg-green-500 text-green-900'
                            : task.status === 'Em andamento'
                            ? 'bg-yellow-500 text-yellow-900'
                            : 'bg-red-500 text-red-900'
                        }`}
                      >
                        {task.status}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* Empty State */}
      {totalSubjects === 0 && totalTasks === 0 && (
        <section className="py-12 text-center">
          <div className="max-w-xl mx-auto px-4">
            <h2 className="text-2xl font-bold mb-4">🚀 Comece agora!</h2>
            <p className="mb-6 text-gray-400">
              Você ainda não tem dados cadastrados. Use o menu lateral para:
            </p>
            <div className="space-y-3 text-left">
              <p className="flex items-start">
                <span className="flex-shrink-0 text-gray-400">•</span>
                <span className="ml-3">
                  <a
                    href="/disciplinas"
                    className="text-blue-400 underline hover:text-blue-300"
                  >
                    Disciplinas
                  </a>{' '}
                  → Cadastre suas matérias
                </span>
              </p>
              <p className="flex items-start">
                <span className="flex-shrink-0 text-gray-400">•</span>
                <span className="ml-3">
                  <a
                    href="/tarefas"
                    className="text-blue-400 underline hover:text-blue-300"
                  >
                    Tarefas
                  </a>{' '}
                  → Adicione suas tarefas e prazos
                </span>
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Footer - Optional - could add navigation or additional info */}
      <footer className="py-6 border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
          EduTrack AI • Desenvolvido para a Faculdade Impacta
        </div>
      </footer>
    </div>
  );
}

// Helper function to get subject color (consistent with subjects page)
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