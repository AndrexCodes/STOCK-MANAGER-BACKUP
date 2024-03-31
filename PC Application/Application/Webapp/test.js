const persons = [
    {name: 'John', age: 30},
    {name: 'Alice', age: 25},
    {name: 'Bob', age: 40}
]; // Example object containing persons' details

const listOfNames = persons.map(person => person.name);
console.log(listOfNames); // Output: ['John', 'Alice', 'Bob']