with open('data/spo_data.txt', 'r', encoding='utf-8') as infile, open('data/spo_data.spo', 'w', encoding='utf-8') as outfile:
    for line in infile:
        subject, predicate, object = line.strip().split(',')  # 假设三元组由制表符分隔
        outfile.write(f"{subject}\t{predicate}\t{object}\n")  # 写入.spo文件，可以根据需要调整格式