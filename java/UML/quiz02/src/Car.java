
/**
 *
 * @author alpha4d
 */


interface Drive{
    public void start();
    public void stop();
}

abstract class Vehicle {
    
    
    public String model;

    public Vehicle(String model) {
        this.model = model;
    }
    
    public abstract void display();
    
    
}

class Car extends Vehicle implements Drive{
    
    private final double price;
    
    public Car(String model, double price){
        super(model);
        this.price = price;
    }
    
    @Override
    public void display(){
         System.out.println("Mode: "+ model);
         System.out.println("Price: "+ price);
     }
    
    @Override
    public void start(){
        System.out.println(model+" is starting..");
    }
    
    @Override
    public void stop(){
        System.out.println(model+" is stoping..");
    }
    
    public static void main(String[] args){
        Car car = new Car("S3", 20000.32);
        
        car.display();
        System.out.println();
        car.start();
        car.stop();
    }
}

