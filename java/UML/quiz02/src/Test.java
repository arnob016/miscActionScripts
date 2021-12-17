
/**
 *
 * @author alpha4d
 */


abstract class Animal{
    protected String name;

    public Animal(String name) {
        this.name = name;
    }
    
    public abstract void move();
    
}

class Bird extends Animal{
    
    private final String color;
    
    public Bird(String name, String color) {
        super(name);
        this.color = color;
    }
    
    @Override
    public void move(){
        System.out.println(name+" is moving.");
        System.out.println(name+" color is "+color);
    }

    
}

class Fish extends Animal{
    
    private final String size;
    
    public Fish(String name, String size) {
        super(name);
        this.size = size;
    }
    
    @Override
    public void move(){
        System.out.println(this.name+" is moving.");
        System.out.println(name+" size is "+size);
    }
    
}


public class Test {

    public static void main(String[] args) {
        Bird bd = new Bird("Doyel", "red");
        bd.move();
        
        System.out.println();
        
        Fish fh = new Fish("Rui", "big");
        fh.move();
    }
    
}
