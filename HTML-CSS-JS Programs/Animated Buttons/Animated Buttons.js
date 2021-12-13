document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault()
    return false
  })
})
