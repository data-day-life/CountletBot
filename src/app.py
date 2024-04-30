from bot import helpers

f_name = 'cold_boot_count_history--2024-04-30__13-51-21.pk'
results = helpers.load_pickle_results(f_name, verbose=True)
[print(r) for r in results]

print()

