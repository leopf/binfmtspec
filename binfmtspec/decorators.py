from binfmtspec.spec import BinarySpec

id_counter = 0

def binary_spec_component(name: str):
    global id_counter

    rcd_id = id_counter
    id_counter += 1
    
    def binary_spec_component_dec(func):
        def inner(s: BinarySpec, *args):
            is_recursion = s.start_rcd(rcd_id)
            if is_recursion:
                s.start_scope("{} (recursive)".format(name))
                s.add_recursive()
            else:
                s.start_scope(name)
                func(s, *args)

            s.end_scope()
            s.end_rcd()
        
        return inner
    return binary_spec_component_dec