// const $ = (selector, all=false) => all ? document.querySelectorAll(selector) : document.querySelector(selector)

// Links to w3.org for SVG Elements
const svg_link = "http://www.w3.org/2000/svg"

/**
 * Custom JQuery kinda function, providing shorthand stuff
 * Flags:
 *     'q' : [default] Shorthand for document.querySelector
 *     '+' :           Shorthand for document.querySelectorAll
 *     'c' :           Shorthand for document.createElement
 *     's' :           Shorthand for document.createElementNS
 *     'p' :           Shorthand for document.elementFromPoint
 *     'p+':           Shorthand for document.elementsFromPoint
 * @param  {String} args  Depending on the flag, it can be a selector, or an element to create
 * @param  {String} flags Flags to control the function
 * @return {object}
 */
export default function $(args, flags='q') {
    if (typeof(args) !== 'string') throw "Invalid Argument Type. Supported types are only \"string\""
    if (typeof(flags) !== 'string') throw "Invalid Flag Type. Supported types are only \"string\""
    if (!['q', '+', 'c', 's', 'p', 'p+'].includes(flags)) throw "Unknown Flag!!!"
    switch(flags) {
        case 'q':
            return document.querySelector(args)
        case '+':
            return document.querySelectorAll(args)
        case 'c':
            return document.createElement(args)
        case 's':
            return document.createElementNS(svg_link, args)
        case 'p':
        {
            const [x, y] = args.split(', ').map(e => parseFloat(e))
            return document.elementFromPoint(x, y)
        }
        case 'p+':
        {
            const [x, y] = args.split(', ').map(e => parseFloat(e))
            return document.elementsFromPoint(x, y)
        }
    }
}


export function memoize(func) {
    const cache = {}
    function call(...args) {
        const str_args = JSON.stringify(args)
        if (!cache[str_args]) {
            cache[str_args] = func(str_args)
        }
        return cache[str_args]
    }

    return call
}

export function track_time(func) {
    return (...args) => {
        console.time(func.name)
        const result = func(...args)
        console.timeEnd(func.name)
        return result
    }
}
