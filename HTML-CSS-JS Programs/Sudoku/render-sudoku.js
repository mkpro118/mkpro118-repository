class Square extends HTMLElement {
    constructor() {
        super()
    }

    connectedCallback() {
        this.classList.add('normal')
        this.innerHTML = `
            <svg width="100%" height="100%" viewBox="0 0 100 100" style="position:relative;z-index:1100;">
                <circle class="empty" cx="50" cy="50" r="40%" />
                <text x="50%" y="56.9%" dominant-baseline="middle" text-anchor="middle" class="text"></text>
            </svg>
        `
    }
}

class SubGrid extends HTMLElement {
    constructor() {
        super()
    }

    connectedCallback() {
        this.style = `
            display: grid;
            grid-template-rows: 1fr 1fr 1fr;
            grid-template-columns: 1fr 1fr 1fr;
            z-index: 1000;
            grid-gap: 1.1%;
            height: 100%;
            width: 100%;
            position: relative;
        `
        for (let i = 1; i <= 9; i++) {
            this.appendChild(document.createElement('game-square'))
        }
    }
}

class SudokuBoard extends HTMLElement {
    constructor() {
        super()
    }

    connectedCallback() {
        this.style = `
            display: grid;
            grid-template-rows: 1fr 1fr 1fr;
            grid-template-columns: 1fr 1fr 1fr;
            height: 100%;
            width: 100%;
            grid-gap: 0.5%;
            position: relative;
            border: 2px solid hsl(206, 55%, 15%);
            box-shadow: 0 0 15px 3px hsl(200 89% 60%);
        `


        for (let i = 1; i <= 9; i++) {
            this.appendChild(document.createElement('sub-grid'))
        }
    }
}

class GameNumbers extends HTMLElement {
    constructor() {
        super()
    }

    connectedCallback() {
        this.style = `
            height: 100%;
            width: 100%;
            display: flex;
            box-shadow: 0 0 10px 2px hsl(200 89% 60%);
        `

        this.innerHTML = ``
        for (let i = 1; i < 10; i++) {
            this.innerHTML += `
                <div style="width:calc(100% / 9);height:100%;">
                    <svg width="100%" height="100%" viewBox="0 0 100 100">
                        <circle cx="50%" cy="50%" r="40%" style="fill:transparent;stroke: #0AF;stroke-width:2%;" />
                        <text x="50%" y="56.9%" dominant-baseline="middle" text-anchor="middle" class="number-text">
                            ${i}
                        </text>
                    </svg>
                </div>
            `
        }
    }
}

class GameTools extends HTMLElement {
    constructor() {
        super()
    }

    connectedCallback() {
        this.style = `
            height: 100%;
            width: 70vh;
            display: flex;
            justify-content: space-between;
            align-items: center;
        `

        this.innerHTML = `
        <svg width="20%" height="69%" viewBox="0 0 24 24">
        <path d="M17.026 22.957c10.957-11.421-2.326-20.865-10.384-13.309l2.464 2.352h-9.106v-8.947l2.232 2.229c14.794-13.203 31.51 7.051 14.794 17.675z"/>
        </svg>
        <svg id="reset-puzzle" width="20%" height="80%" viewBox="0 0 24 24">
        <path d="M13.5 2c-5.629 0-10.212 4.436-10.475 10h-3.025l4.537 5.917 4.463-5.917h-2.975c.26-3.902 3.508-7 7.475-7 4.136 0 7.5 3.364 7.5 7.5s-3.364 7.5-7.5 7.5c-2.381 0-4.502-1.119-5.876-2.854l-1.847 2.449c1.919 2.088 4.664 3.405 7.723 3.405 5.798 0 10.5-4.702 10.5-10.5s-4.702-10.5-10.5-10.5z"/>
        </svg>
        <label style="width:50%; height:100%;display:flex;justify-content:center; align-items:center;margin-right:2.5%;">
            <svg width="75%" height="80%" viewBox="0 0 100 100">
                <text x="50%" y="56.9%" dominant-baseline="middle" text-anchor="middle" class="autocheck">AutoCheck</text>
            </svg>
            <input type="checkbox" id="auto-check">
            <span class="toggle-btn">

            </span>
        </label>
        <select>
            <option value="Easy" selected>Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
            <option value="Expert">Expert</option>
        </select>
        `
    }
}

async function render() {
    customElements.define('game-square', Square)
    customElements.define('sub-grid', SubGrid)
    customElements.define('sudoku-board', SudokuBoard)
    customElements.define('game-numbers', GameNumbers)
    customElements.define('game-tools', GameTools)

    let c = 0

    for (let j = 2; j <= 4; j++) {
        document.querySelectorAll(`sub-grid:nth-child(3n+${j})`)
        .forEach(e => {
            for (let i = 1; i <= 3; i++) {
                e.querySelectorAll(`game-square:nth-child(3n+${i})`)
                .forEach( f => {
                    f.dataset.col = `${c+i}`
                })
            }
        })
        c += 3
    }

    c = 1

    for (let i = 1; i < 10; i++) {
        document.querySelectorAll(`game-square[data-col="${i}"]`)
        .forEach(e => {
            e.dataset.row = `${c++}`
        })
        c = 1
    }



    document.querySelectorAll('game-square')
    .forEach(e => {
        e.id = e.dataset.row + e.dataset.col
    })
}
