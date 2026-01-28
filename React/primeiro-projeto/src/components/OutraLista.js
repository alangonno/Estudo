function OutraLista({ itens }) {
    return (
        <>
            <h3>Lista: </h3>
            {itens.map((item) => (
                <p>{item}</p>
            ))}
        </>
    )
}

export default OutraLista;