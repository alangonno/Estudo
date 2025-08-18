import HelloWorld from './components/HellowWorld';
import './App.css';
import SayMyName from './components/SayMyName';
import Pessoa from './components/Pessoa';
import Frase from './components/Frase';
import List from './components/List';

function App() {

  return (
    <div className="App">
      <Frase />
      <HelloWorld />
      <SayMyName nome="Alan"/>
      <SayMyName nome="Joao"/>
      <Pessoa 
        nome="Alan" 
        idade="18" 
        profissao="Dev"
      />
      <List />
    </div>
  );
}
 
export default App;
