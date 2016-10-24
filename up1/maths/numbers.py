def isPrime(n):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False
    for i in range(3,int(n**0.5)+1,2):   # only odd numbers
        if n%i==0:
            return False
    return True

def isPandigital(k, n):
    # is n k-pandigital?
    l = [str(i) for i in range(0,k+1)]
    n = str(n)
    if k+1 == len(n):
        for c in str(n):
            if c in l:
                l.remove(c)
            else:
                return(False)
        return(True)
    else:
        return(False)
