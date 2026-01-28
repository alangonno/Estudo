import './App.css';
import Evento from './components/Evento';
import Form from './components/Form';
import OutraLista from './components/OutraLista';
function App() {

  const meusItens = ['react', 'java', 'sql']

  return (
    <div className="App">
      <Evento />
      <Evento numero={2} />
      <Form />   
      <OutraLista itens={meusItens}/>   
    </div>
  );
}
 
export default App;
