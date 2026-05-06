from DatasetCreator import DatasetCreator
from Plotter import Plotter


def main():
    creator = DatasetCreator(t_span=[0, 500], dt=0.1, amp_range=(3, 9), noise_level=0.0)
    dataset = creator.create_dataset(n_aprbs=10, n_multisine=10, n_noise=10)

    for category, signals in dataset.items():
        print(f"\n=== Kategoria: {category.upper()} ===")
        for i, traj in enumerate(signals[:2]):  # Pokazujemy tylko 2 przykłady
            print(f"Trajektoria nr {i+1}:")
            print(f"  t (pierwsze 5): {traj.t[:5]}")
            print(f"  y (pierwsze 5): {traj.y[:5]}")
            print(f"  Długość wektora: {len(traj.y)} próbek")
            print("-" * 30)

    # Rysowanie
    # Chcę porównać pierwszy, środkowy i ostatni sygnał ze wszystkich kategorii 
    Plotter.plot_indices(dataset['aprbs'], "aprbs", indices=[0, 5, 9])

    Plotter.plot_indices(dataset['multisine'], "multisine", indices=[0, 5, 9])

    Plotter.plot_indices(dataset['noise'], "noise", indices=[0, 5, 9])


if __name__ == "__main__":
    main()