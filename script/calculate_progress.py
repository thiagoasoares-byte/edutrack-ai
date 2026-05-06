import sys
import json

def calculate_progress(tasks):
    """
    Calcula o progresso com base em uma lista de tarefas.

    Args:
        tasks (list): Uma lista de dicionários de tarefas. Espera-se que cada
                      dicionário tenha uma chave 'status'.

    Returns:
        dict: Um dicionário contendo total_tasks, completed_tasks,
              e progress_percentage.
    """
    total_tasks = len(tasks)

    if total_tasks == 0:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "progress_percentage": 0.0
        }

    # Conta as tarefas com status 'done'
    completed_tasks = sum(1 for task in tasks if task.get('status') == 'done')

    progress_percentage = (completed_tasks / total_tasks) * 100

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": round(progress_percentage, 2)
    }

def main():
    """
    Função principal para ler do stdin, calcular o progresso e imprimir para stdout.
    """
    try:
        input_data = sys.stdin.read()
        tasks = json.loads(input_data)
        result = calculate_progress(tasks)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, TypeError):
        print(json.dumps({"error": "Invalid JSON format received."}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

