#include<cstdio>
#include<string>
#include<iostream>

using namespace std;

// gcc -c x.cpp 只编译x.cpp
// gcc -o x.cpp x.exe 编译和链接并指定输出文件为x.exe

void fun()
{
    printf("hello");
}


class A
{
public:
    int x = 10; // 在c++ 11之前,是不允许在类内直接赋值的,c++ 11则可以了
    static int y;
    A(int x = 0)
    {
        this->x = x;
    }
    void fun()
    {
        printf("x=%d, y=%d\n", x,y);
    }
};
int A::y = 10;

class C
{
public:
    int a = 8888;
};

class B:A,public C  // B私有继承A,公有继承C,此处不能保护继承C,否则c.a在main中不可见
                    // 私有继承,父类公有和保护成员变成子类的私有成员,保护继承则变成保护成员
                    // 无论是什么继承方式,都不会改变子类对父类成员的访问权限
{
public:
    void fun(int gg)
    {
        printf("gg=%d, hhhhhr!\n", gg);
        A::fun(); // 访问父类成员,用父类的名字来限定
    }
};

extern int a;
void ff()
{
    a += 100; // 此句语法出错,显示a没有定义(除非加上第30句的extern语句),这和python不同,python中只要全局变量定义
              // 在函数调用语句之前即可,不需要定义在函数定义之前 
    printf("a=%d\n", a);
}
int a = 10;

int main()
{
    // 01 
    printf("%c\n", 0x7c); // 0x7c是'|'
    
    // 02
    float a = -5/3;
    float b = 5/3;
    cout << a << b << endl;  // a=-1,b=1直接去除小数部分(向零取整)
    
    // 03
    123;    // 无语法错误,说明c也和python一样,一个语句可以是一个单独的常量
    "hello \
        shshsh";
    
    // 04
    int c = 10;
    printf("%p\n", &c);
    c = 100;
    printf("%p\n", &c); // 地址一样,说明是修改值,而不是修改地址,不同于python

    string d = "hello";
    printf("%p\n", &d);
    d = d + "world";
    printf("%p\n", &d); // 地址一样
    
    // 05
    int fun = 100;
    //fun(); // 此句有语法错误,将fun当作变量而不是函数了,这与python一样
             // 这是因为fun()是全局标识符,而int fun 则是局部变量
             // 所以里层标识符屏蔽了外层同名标识符,而会出现标识符重定义错误
    
    //06 
    if(1)
    {
        int d6 = 100;
    }
    {
        float d61 =10.;
    }
    //printf("%d", d6);     // 此两句发出两个变量没有定义的错误
    //printf("%f", d61);    // 说明C++中{}是一个新的作用域,这不同于python
    
    //07 
    A aa = A(66);
    aa.fun();   // 在fun中可以直接使用类的属性,说明类作用域是方法作用域的全局空间,这不同于python
                // 在python中,类属性是不能直接在方法中使用的,必须用类名或者self来调用
    // 08  
    ff(); // 也说明变量的使用范围是从定义处到结束,而不是这个作用域,和python一样

    
    // 09
    B bb = B();
    bb.fun(100); // 此处不能写fun(),因为B类中并没有fun(),虽然父类A中有fun(),所以子类对象调用时
                 // 其实是屏蔽掉了基类同名函数的
    printf("bb.a=%d\n", bb.a);

    return 0;
}
