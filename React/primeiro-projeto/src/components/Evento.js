import Button from "./Button";
function Evento({numero}) {

    function meuEvento() {
        console.log("evento ativado " + numero)
        }
    
    function segundoEvento() {
        console.log("Segundo evento ativado")
    }

    return (
        <div>
            <p>Disparar evento</p>
            <Button event={meuEvento} text="Primeiro" />
            <Button event={segundoEvento} text="Segundo evento" />
        </div>
    );
}

export default Evento;