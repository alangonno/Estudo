import Item from './Item';

function List() {
    return(
        <>
            <h1>Minha Lista</h1>
            <ul>
                <Item 
                    marca="Nike" 
                    lancamento={1900} 
                    />
                <Item 
                    marca="Puma" 
                    lancamento={1980} 
                    />
                <Item 
                    marca="Adidas" 
                    lancamento={1950} 
                />
                <Item />
            </ul>
        </>
    );
}


export default List;