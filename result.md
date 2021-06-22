## 제목을 입력하세요...
```mermaid
classDiagram
class Abstraction{
<<private>>
     +implementation) * Abstraction() * Abstraction(IImplementation
     +Operation() * string
}

class ExtendedAbstraction{
<<private>>
     +implementation) : base() : base(implementation) * ExtendedAbstraction(IImplementation
     +Operation() * string
}

class IImplementation{
<<interface>>
        OperationImplementation() * string
}

class ConcreteImplementationA{
<<private>>
     +OperationImplementation() * string
}

class ConcreteImplementationB{
<<private>>
     +OperationImplementation() * string
}

class Client{
<<private>>
     +ClientCode() * void
}

class Program{
<<private>>
     -Main() * void
}

Abstraction<|--ExtendedAbstraction: Inheritance
IImplementation<|--ConcreteImplementationA: Inheritance
IImplementation<|--ConcreteImplementationB: Inheritance
