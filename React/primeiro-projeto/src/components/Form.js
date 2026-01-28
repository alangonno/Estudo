import { useState } from "react";

function Form() {

    function cadastrarUsuario(e) {
        e.preventDefault()
        console.log(name)
        console.log(password)
        console.log("Usuario cadastrado")
    }

    const [name, setName] = useState()
    const [password, setPassword] = useState()

    return(
        <div>
            <form onSubmit={cadastrarUsuario}>
                <div>
                    <label htmlFor="name"></label>
                    <input id="name" name="name" type="text" placeholder="DIgite seu nome" onChange={(e) => setName(e.target.value)}></input>
                </div>
                <div>
                    <label htmlFor="senha"></label>
                    <input 
                    id="senha" name="senha" type="password" placeholder="DIgite sua senha" onChange={(e) => setPassword(e.target.value)}></input>
                </div>
                <div>
                    <input type="submit" value="Cadastrar"></input>
                </div>
            </form>
        </div>
    )
}

export default Form;