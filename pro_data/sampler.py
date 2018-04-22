import random

def random_sampler(in_file, out_file, samples):
    with open(in_file, 'r') as f_i:
        n_lines = sum(1 for line in f_i)
        f_i.seek(0)

        f_o = open(out_file, 'w')
        r_lines = sorted(random.sample(range(n_lines), samples), reverse = True)
        next_line = r_lines.pop()
        for index, line in enumerate(f_i):
            if index == next_line:
                f_o.write(line)
                if len(r_lines) > 0:
                    next_line = r_lines.pop()
                else:
                    break
