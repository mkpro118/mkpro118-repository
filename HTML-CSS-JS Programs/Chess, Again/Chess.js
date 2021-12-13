import $ from '../My JQuery.js'

const ranks = [1, 2, 3, 4, 5, 6, 7, 8,]
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',]
const piece_init_list = []

function* reversed(args) {
    let i = args.length
    while (i) {
        yield args[--i]
    }
}

function* range(...args) {
    let [start, stop, step] = [0, 0, 1];
    switch(args.length) {
        case 1:
            stop = args[0]
            break;
        case 1:
            start = args[0]
            stop = args[1]
            break;
        case 1:
            start = args[0]
            stop = args[1]
            step = args[2]
            break;
        default:
            throw new 'Too many arguments'
    }
    while (start < stop) {
        yield start
        start += step
    }
}

function* zip(...args) {
    let s = args[0].length
    for(let arg of args) s = arg.length < s ? arg.length : s

    let i = 0
    while (i < s) {
        list = []
        for(let arg of args) list.push(arg[i])
        yield list
        i++
    }
}

class Board extends HTMLElement {
    constructor() {
        super()
        this.boardStates = {}
        this.moves = []
        this.turn = 'white'
        this.moveNumber = 1
        this.movesList = this._movesList()
        this.movesList.next()
    }

    // methods
    connectedCallback() {
        {
            const span = $('span', 'c')
            span.classList.add('ranks-text')
            for (let i of ranks) {
                const text = $('span', 'c')
                text.innerText = `${9-i}`
                span.appendChild(text)
            }
            this.appendChild(span)

        }

        {
            const span = $('span','c')
            span.classList.add('files-text')
            for (let f of files) {
                const text = $('span', 'c')
                text.innerText = `${f}`
                span.appendChild(text)
            }
            this.appendChild(span)
        }


        let count = 0
        for(let rank of reversed(ranks)) {
            for(let file of files) {
                const _class = count++ % 2 === 0 ? "light" : "dark"
                const sq = $(`${_class}-square`,'c')
                sq.classList.add('chess-square')
                sq.setAttribute('id', `${file}${rank}`)
                this.appendChild(sq)
            }
            count++
        }
    }

    init() {
        for (let piece of this.__pieceInitialiser()) {
            const sq = $(`#${piece.init_pos}`)
            const p = $(`chess-piece`, 'c')
            p.addPiece(piece)
            sq.appendChild(p)
        }
    }

    * __pieceInitialiser() {
        for (let file of files) {
            yield new Pawn('white', `${file}2`)
            yield new Pawn('black', `${file}7`)
        }
        for (let file of ['c', 'f']) {
            for (let rank of [1, 8]) {
                yield new Bishop(`${rank === 1 ? 'white' : 'black'}`, `${file}${rank}`)
            }
        }
        for (let file of ['b', 'g']) {
            for (let rank of [1, 8]) {
                yield new Knight(`${rank === 1 ? 'white' : 'black'}`, `${file}${rank}`)
            }
        }
        for (let file of ['a', 'h']) {
            for (let rank of [1, 8]) {
                yield new Rook(`${rank === 1 ? 'white' : 'black'}`, `${file}${rank}`)
            }
        }
        for (let rank of [1, 8]) {
            yield new Queen(`${rank === 1 ? 'white' : 'black'}`, `d${rank}`)
        }
        for (let rank of [1, 8]) {
            yield new King(`${rank === 1 ? 'white' : 'black'}`, `e${rank}`)
        }
    }

    * _movesList() {
        while (true) {
            const move = yield
            if (!move || !(typeof move === 'string') || !move.match(/[BKNQR]?[a-h]{1}[1-8]{1}/gi)) {
                throw "yo what's this move"
            }
            this.moves.push(move)
            this.boardStates[`${this.moveNumber}${this.turn[0]}`] = this.innerHTML
            if (this.turn === 'black') {
                this.moveNumber++
                this.turn = 'white'
            } else {
                this.turn = 'black'
            }
        }
    }

    getBoardState(move) {
        return this.boardStates[`${move}`]
    }

    getCurrentBoardState() {
        const move = this.turn === 'black' ? `${this.moveNumber}w` : `${this.moveNumber-1}b`
        return this.boardStates[`${move}`]
    }

    getCurrentBoardStateArray() {
        const arr = new Array(8).fill(null).map(e => new Array(8).fill(''))
        console.log(arr)
        for(let piece of $('chess-piece', '+')) {
            const [x, y] = piece.piece.getCurrentPositionIndex()
            arr[7-y][x] = `${piece.piece.color}-${piece.piece.name}`
        }
        return [...arr]
    }

    setInitialBoardState() {
        this.boardStates.start = this.innerHTML
    }

    reset() {
        for(let e of this.querySelectorAll('chess-piece')) {
            e.remove()
        }
        this.init()
    }
}

class Square extends HTMLElement {
    constructor() {
        super()
        this.color;
    }

    connectedCallback() {
        this.style.setProperty('background', `--${this.color}`)
        const highlight_layer = $('span', 'c')
        highlight_layer.classList.add('highlight-layer')
        const check_highlight_layer = $('span', 'c')
        check_highlight_layer.classList.add('check-highlight-layer')
        this.appendChild(highlight_layer)
        this.appendChild(check_highlight_layer)
    }

    clearPieces() {
        let removed = false
        while (true) {
            const inner = this.querySelector('chess-piece')
            if(inner) {
                this.removeChild(inner)
                removed = true
            }
            else {
                break
            }
        }
        return removed
    }
}

class LightSquare extends Square {
    constructor() {
        super()
        this.color = 'light'
    }
}

class DarkSquare extends Square {
    constructor() {
        super()
        this.color = 'dark'
    }
}

customElements.define('light-square', LightSquare)
customElements.define('dark-square', DarkSquare)
customElements.define('chess-board', Board)

class ChessPiece extends HTMLElement {
    constructor() {
        super()
        this.piece
        this.pieceName
        this.isDown = false
        this.mouseMoved = false
    }

    connectedCallback() {
        this.addEventListener('mousedown', this.mousedown)
        this.addEventListener('mouseup', this.mouseup)
        this.addEventListener('click', this.clicked)
    }

    addPiece(piece) {
        this.piece = piece
        this.pieceName = this.piece.name
        this.dataset.pieceName = this.pieceName
        this.dataset.pieceColor = this.piece.color
        this.style.setProperty('background-image', `url("${this.piece.img}")`)
    }

    moveTo(sq) {
        const removed = sq.clearPieces()
        const pawn = (this.piece.name === 'pawn' && removed) ? `${this.parentNode.id[0]}` : ''
        sq.appendChild(this)
        return pawn + (removed ? 'x' : '')
    }

    clicked() {
        if (!this.mouseClicked) return
        event.stopPropagation()
    }

    mousedown(event) {
        this.isDown = true
        event.stopPropagation()
        if (board.turn !== this.piece.color) return;
        const rect = this.getBoundingClientRect()
        this.x = event.clientX - rect.left
        this.y = event.clientY - rect.top
        this.addEventListener('mousemove', this.mousemove)
        this.style.setProperty('cursor', 'grabbing')
        this.style.setProperty('--z', '9')
    }

    mouseup(event) {
        if (!(this.isDown && this.mouseMoved)) {
            this.revert()
            this.mouseClicked = true
            return
        }
        event.stopPropagation()
        event.preventDefault()
        if (board.turn !== this.piece.color) {
            this.revert()
            return;
        }
        this.removeEventListener('mousemove', this.mousemove)
        const square = $(`${event.clientX}, ${event.clientY}`, 'p+').filter(e => e.classList.contains('chess-square'))[0]
        if (!square || square === this.parentNode) {
            this.revert()
            return
        }
        const capture = this.moveTo(square)
        this.piece.moveTo(square.id)

        board.movesList.next(`${this.piece.notation}${capture}${square.id}`)
        this.revert()
    }

    mousemove(event) {
        this.mouseMoved = true
        this.style.setProperty('left', `${event.pageX}px`)
        this.style.setProperty('top', `${event.pageY}px`)
        this.style.setProperty('--x', `-50%`)
        this.style.setProperty('--y', `-50%`)
    }

    mouseout(event) {
        this.mouseup()
    }

    revert() {
        this.isDown = false
        this.mouseMoved = false
        this.style.removeProperty('left')
        this.style.removeProperty('top')
        this.style.removeProperty('--x')
        this.style.removeProperty('--y')
        this.style.removeProperty('--z')
    }
}

customElements.define('chess-piece', ChessPiece)

class Piece {
    constructor(color, init_pos, name) {
        this.color     = color
        this.name      = name
        this.init_pos  = init_pos
        this.img       = `../images/${this.color}-${this.name}-alt.png`
        this.position  = this.init_pos
        this.sliding   = true
        this.offsets   = null
        this.notation  = null
        this.getPossibleMoves = memoize(this.getPossibleMoves).bind(this)
    }

    moveTo(pos) {
        this.position = pos
    }

    getCurrentFileIndex() {
        return files.indexOf(this.position[0])
    }

    getCurrentRankIndex() {
        return ranks.indexOf(+this.position[1])
    }

    getCurrentPositionIndex() {
        return [this.getCurrentFileIndex(), this.getCurrentRankIndex()]
    }

    static getPositionFromIndex(file, rank) {
        return `${files[file]}${ranks[rank]}`
    }

    getPossibleMoves(boardState) {
        console.log(this)
        // const possible_moves = []
        // let [o_file, r_rank] = this.getCurrentPositionIndex()
        // for (let [file_offset, rank_offset] of this.offsets) {
        //     let [c_file, c_rank] = [o_file + file_offset, o_rank + rank_offset]
        //     while((0 <= c_file < 8) && (0 <= c_rank <8)) {
        //         const possible_position = getPositionFromIndex(c_file, c_rank)
        //         // TODO, write the posssible square, check for stuff inside, and then see if it is possible
        //         // const possible_square =
        //         if (!this.sliding) return
        //         [c_file, c_rank] = [c_file + file_offset, c_rank + rank_offset]
        //     }
        // }
    }
}

class Pawn extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos ,'pawn')
        this.sliding = false
        this.notation = ''
        this.offsets = [
            [ 0, 1],
            [-1, 1],
            [ 1, 1],
            [ 0, 2],
        ]
    }

    moveTo(pos) {
        super.moveTo(pos)
        if (this.offsets.length == 4) {
            this.offsets.pop()
        }
    }
}

class Bishop extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos, 'bishop')
        this.notation = 'B'
        this.offsets = [
            [ 1,  1],
            [-1,  1],
            [ 1, -1],
            [-1, -1],
        ]
    }
}

class Knight extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos, 'knight')
        this.sliding = false
        this.notation = 'N'
        this.offsets = [
            [ 1,  2],
            [ 2,  1],
            [-1,  2],
            [-2, -1],
            [-1, -2],
            [-2,  1],
            [ 1, -2],
            [ 2, -1],
        ]
    }
}

class Rook extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos, 'rook')
        this.notation = 'R'
        this.offsets = [
            [-1,  0],
            [ 1,  0],
            [ 0, -1],
            [ 0,  1],
        ]
    }
}

class Queen extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos, 'queen')
        this.notation = 'Q'
        this.offsets = [
            [-1,  0],
            [ 1,  0],
            [ 0, -1],
            [ 0,  1],
            [ 1,  1],
            [ 1, -1],
            [-1,  1],
            [-1, -1],
        ]
    }
}

class King extends Piece {
    constructor(color, init_pos) {
        super(color, init_pos, 'king')
        this.notation = 'K'
        this.offsets = [
            [-1,  0],
            [ 1,  0],
            [ 0, -1],
            [ 0,  1],
            [ 1,  1],
            [ 1, -1],
            [-1,  1],
            [-1, -1],
            [ 2,  0],
            [-2,  0],
        ]
    }
}

const board = $('chess-board')
board.init()
