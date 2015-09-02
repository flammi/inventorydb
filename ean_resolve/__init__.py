import ean_resolve.thalia

RESOLVERS = {
    "Thalia": thalia.resolve_ean,
}

class EANNotResolved(Exception):
    pass

def resolve_ean(*args, **kwargs):
    for storename, func in RESOLVERS.items():
        res = func(*args, **kwargs)
        
        #When the resolver found something -> return result and exit
        if res:
            return res
    #When nothing has been found raise execption
    raise EANNotResolved()
