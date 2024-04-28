def dict_to_csv(data, filename):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, data.keys())
        writer.writeheader()
        writer.writerow(data)