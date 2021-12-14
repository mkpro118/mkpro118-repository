class MyJQError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
    if (typeof Error.captureStackTrace === 'function') {
      Error.captureStackTrace(this, this.constructor);
    } else {
      this.stack = (new Error(message)).stack;
    }
  }
}

class MyJQInvalidSelectorError extends MyJQError {}
class MyJQIllegalArguementError extends MyJQError {}
class MyJQIndexOutOfBoundsError extends MyJQError {}
class MyJQElementCreationError extends MyJQError {}

class NodeWrapper {
    constructor(n) {
        this.n = n
        return NodeWrapper.#proxify(this)
    }

    click() {
        this.n.click()
        return this
    }

    html(t) {
        if (!t) return this.n.innerHTML
        this.n.innerHTML = `${t}`
        return this
    }

    text(t) {
        if (!t) return this.n.innerText
        this.n.innerText = `${t}`
        return this
    }

    css(p, v) {
        if (!p) return this.n.style
        if (!v) return getComputedStyle(this.n).getPropertyValue(`${p}`)
        this.n.style.setProperty(`${p}`, `${v}`)
        return this
    }

    on(e, c, u) {
        if (!e || !c) throw new Exception("Cannot bind event")
        this.n.addEventListener(e, c, u)
        return this
    }

    append(...n) {
        for(let _ of n) {
            this.n.appendChild(_)
        }
        return this
    }

    appendTo(n) {
        let k
        if (typeof n === 'string') k = (new MyJQ(n, {__str__:true})).get()
        else k = n
        k.appendChild(this.n)
        return this
    }

    get() {return this.n}

    addClass(...c) {
        if (!c) throw new MyJQIllegalArguementError(`Cannot add class ${c}`)
        for(let _ of c) {
            this.n.classList.add(_)
        }
    }

    removeClass(...c) {
        if (!c) throw new MyJQIllegalArguementError(`Cannot add class ${c}`)
        for(let _ of c) {
            this.n.classList.remove(_)
        }
    }

    static #proxify(t) {
        return new Proxy(t, {
            get: (_t, p, r) => {
                return (p in _t) ? _t[p] : t.n[p]
            }
        })
    }
}


class MyJQ {
    #nl
    constructor (n, o) {
        if (!o.__str__) {
            return new NodeWrapper(n)
        }
        delete o.__str__
        if (n.startsWith('<') && n.endsWith('>')) {
            return MyJQ.__create__(n.slice(1,-1), o)
        }
        try {
            this.#nl = [...document.querySelectorAll(n)]
        }
        catch (err) {
            throw new MyJQInvalidSelectorError("Invalid Selector")
        }
        this.#wrap()
        return this.#nl.length == 1 ? this.first() : this
    }

    first() {return this.#nl[0]}

    last() {return this.#nl[this.#nl.length - 1]}

    nth(n) {
        n = parseInt(n)
        if (isNaN(n)) throw new MyJQIllegalArguementError("Illegal Argument")
        n += n < 0 ? this.#nl.length : 0
        if (!(0 < n < this.#nl.length)) throw new MyJQIndexOutOfBoundsError("Index Out Of Bounds")
        return this.#nl[n]
    }

    each(c) {
        if (typeof c !== 'function') throw new MyJQIllegalArguementError("Illegal Argument")
        for(let _ of this.#nl) {
            c(_)
        }
        return this
    }

    static __create__(n, o) {
        let _
        try {
            _ =  new NodeWrapper(document.createElement(n))
        }
        catch (err) {
            console.log(err)
            throw new MyJQElementCreationError(`Cannot create element ${n}`)
        }
        for(let __ of Object.keys(o)) {
            console.log(__)
            _.get()[__] = o[__]
        }
        return _
    }

    #wrap() {
        this.#nl = this.#nl.map(_ => new NodeWrapper(_))
    }

    getList() {return this.#nl}

    length() {return this.#nl.length}

    css(p, v) {
        if (!p || !v) throw new MyJQIllegalArguementError("Poperty and Value must be specified")
        for(let _ of this.#nl) {
            _.css(p, v)
        }
    }
}

export default function $(args, options={}) {
    if (typeof args === 'string')
        options.__str__ = true
    else
        options.__str__ = false
    return new MyJQ(args, options)
}





// // const $ = (selector, all=false) => all ? document.querySelectorAll(selector) : document.querySelector(selector)

// // Links to w3.org for SVG Elements
// const svg_link = "http://www.w3.org/2000/svg"

// /**
//  * Custom JQuery kinda function, providing shorthand stuff
//  * Flags:
//  *     'q' : [default] Shorthand for document.querySelector
//  *     '+' :           Shorthand for document.querySelectorAll
//  *     'c' :           Shorthand for document.createElement
//  *     's' :           Shorthand for document.createElementNS
//  *     'p' :           Shorthand for document.elementFromPoint
//  *     'p+':           Shorthand for document.elementsFromPoint
//  * @param  {String} args  Depending on the flag, it can be a selector, or an element to create
//  * @param  {String} flags Flags to control the function
//  * @return {object}
//  */
// export default function $(args, flags='q') {
//     if (typeof(args) !== 'string') throw "Invalid Argument Type. Supported types are only \"string\""
//     if (typeof(flags) !== 'string') throw "Invalid Flag Type. Supported types are only \"string\""
//     if (!['q', '+', 'c', 's', 'p', 'p+'].includes(flags)) throw "Unknown Flag!!!"
//     switch(flags) {
//         case 'q':
//             return document.querySelector(args)
//         case '+':
//             return document.querySelectorAll(args)
//         case 'c':
//             return document.createElement(args)
//         case 's':
//             return document.createElementNS(svg_link, args)
//         case 'p':
//         {
//             const [x, y] = args.split(', ').map(e => parseFloat(e))
//             return document.elementFromPoint(x, y)
//         }
//         case 'p+':
//         {
//             const [x, y] = args.split(', ').map(e => parseFloat(e))
//             return document.elementsFromPoint(x, y)
//         }
//     }
// }
