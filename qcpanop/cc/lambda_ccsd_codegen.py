# ccsd lambda equations
# L = <0| (1+L) e(-T) H e(T) |0>
# dL/dtu = <0| e(-T) H e(T) |u> + <0| L e(-T) H e(T) |u> - <0| L tu e(-T) H e(T) |0>

import pdaggerq

from pdaggerq.parser import contracted_strings_to_tensor_terms


def main():
    pq = pdaggerq.pq_helper("fermi")
    pq.set_print_level(0)

    print('')
    print(
        '    0 = <0| e(-T) H e*f*nm e(T)|0> + <0| L e(-T) [H, e*f*nm] e(T)|0>')
    print('')

    #  <0| e(-T) H e*f*nm e(T)|0>

    pq.set_left_operators([['1']])
    pq.set_right_operators([['1']])

    pq.add_st_operator(1.0, ['f', 'e2(e,f,n,m)'], ['t1', 't2'])
    pq.add_st_operator(1.0, ['v', 'e2(e,f,n,m)'], ['t1', 't2'])

    # <0| L e(-T) [H,e*f*nm] e(T)|0>

    pq.set_left_operators([['l1'], ['l2']])

    pq.add_st_operator(1.0, ['f', 'e2(e,f,n,m)'], ['t1', 't2'])
    pq.add_st_operator(1.0, ['v', 'e2(e,f,n,m)'], ['t1', 't2'])

    pq.add_st_operator(-1.0, ['e2(e,f,n,m)', 'f'], ['t1', 't2'])
    pq.add_st_operator(-1.0, ['e2(e,f,n,m)', 'v'], ['t1', 't2'])

    pq.simplify()

    # grab list of fully-contracted strings, then print
    doubles_residual_terms = pq.fully_contracted_strings()
    for my_term in doubles_residual_terms:
        print(my_term)
    doubles_residual_terms = contracted_strings_to_tensor_terms(
        doubles_residual_terms)
    for my_term in doubles_residual_terms:
        print("#\t", my_term)
        print(my_term.einsum_string(update_val='lambda_two',
                                    output_variables=('m', 'n', 'e', 'f')))
        print()

    pq.clear()


if __name__ == "__main__":
    main()
