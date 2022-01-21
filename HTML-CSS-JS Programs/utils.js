function memoize(func) {
    const cache = {}
    return (...args) => {
        const str_args = JSON.stringify(args)
        if (!cache[str_args]) {
            cache[str_args] = func(str_args)
        }
        return cache[str_args]
    }
}

function track_time(func) {
    return (...args) => {
        console.time(func.name)
        const result = func(...args)
        console.timeEnd(func.name)
        return result
    }
}

function* reversed(iterable) {
    let i = list(iterable).length
    while (i) {
        yield iterable[--i]
    }
}

function* range(...args) {
    let [start, stop, step] = [0, 0, 1];
    switch(args.length) {
        case 1:
            stop = args[0]
            break;
        case 2:
            start = args[0]
            stop = args[1]
            break;
        case 3:
            start = args[0]
            stop = args[1]
            step = args[2]
            break;
        default:
            throw 'Too many arguments'
    }
    while (start < stop) {
        yield start
        start += step
    }
}

function* zip(...iterables) {
    let s = iterables[0].length
    for(let arg of iterables) s = arg.length < s ? arg.length : s

    let i = 0
    while (i < s) {
        list = []
        for(let arg of iterables) list.push(arg[i++])
        yield list
    }
}

function* enumerate(iterable, start=0) {for(const _ of iterable) yield [start++, _]}

function list(iterable) {return [...iterable]}

function any(iterable) {
    for (const _ of iterable) if (_ === true) return true
    return false
}

function all(iterable) {
    for (const _ of iterable) if (_ === false) return false
    return true
}
