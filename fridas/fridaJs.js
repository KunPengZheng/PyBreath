console.log("fridaJs.js loaded successfully ");

/**
 * Java.perform 是 Frida 中用于创建一个特殊上下文的函数，让你的脚本能够与 Android 应用程序中的 Java 代码进行交互。
 * 它就像是打开了一扇门，让你能够访问并操纵应用程序内部运行的 Java 代码。一旦进入这个上下文，你就可以执行诸如钩取方法或访问
 * Java 类等操作来控制或观察应用程序的行为。
 */
Java.perform(function () {
    console.log("Java.perform() start!");

    var packClass = "com.zkp.breath.MainActivity"

    /**
     * var classReference = Java.use("<package_name>.<class>");
     * 使用 Java.use 函数指定要使用的类，该函数接受 包名+类名 作为参数
     */
    var classReference = Java.use(packClass);

    /**
     * <class_reference>.<method_to_hook>.implementation = function(<args>) {};
     * 通过 <class_reference>.<method_to_hook> 符号访问你想要钩取的方法，implementation更改类的方法的实现，<args> 表示传递给函数的参数。
     */
    classReference.fridaTest.implementation = function (x) {
        console.log("original call: fun(" + x + ")");
        send(x); // 将数据发送给主机的python代码
        recv(function (received_json_object) {
            var string_to_recv = received_json_object.my_data
            console.log("string_to_recv: " + string_to_recv);
        }).wait(); //收到数据之后，再执行下去
        const returnValue = this.fridaTest("fe232");// 替换参数
        return returnValue;  // 如果存在返回值，则将返回值返回给原函数
    }

    /**
     * 如果方法存在重载，需要使用overload("int","java.lang.String")函数进行处理所有函数，使用字符串声明参数类型，如果参数非基本类型需要使用
     * "包名 + 类名" 的形式声明。
     */
    // classReference.overloadDemoFun.overload("int", "java.lang.String").implementation = function (x, y) {
    //     console.log("original call: fun(" + x + "," + y + ")");
    //     const string_class = Java.use("java.lang.String"); //获取String类型
    //     /**
    //      * $new()：实例化对象
    //      */
    //     const my_string = string_class.$new("My TeSt String#####");
    //
    //     const returnValue = this.overloadDemoFun(22, my_string);
    //     return returnValue;  // 如果存在返回值，则将返回值返回给原函数
    // }


    /**
     * 修改对象的属性
     */
    classReference.overloadDemoFun.overload("int", "java.lang.String").implementation = function (x, y) {
        console.log("original call: fun(" + x + "," + y + ")");
        const string_class = Java.use("java.lang.String"); //获取String类型
        /**
         * $new()：实例化对象
         */
        const my_string = string_class.$new("My TeSt String#####");
        /**
         * 使用以下方式可以修改对象的属性
         */
        my_string.属性名.value = "sdsds"

        const returnValue = this.overloadDemoFun(22, my_string);
        return returnValue;  // 如果存在返回值，则将返回值返回给原函数
    }


    /**
     * $init：hook构造函数
     */
    // Java.use("com.zkp.breath.bean.Bean").$init.implementation = function (x) {
    //     console.log("original call: fun(" + x + ")");
    //     return this.$init("fe232");  // 如果存在返回值，则将返回值返回给原函数
    // }

    /**
     * Java.choose(className, callbacks)，选择参数一对应的实例，并在找到匹配的实例时执行 onMatch 回调函数，当搜索完成时
     * 执行 onComplete 回调函数。
     * > Java.use()与Java.choose()最大的区别，就是在于前者会新建一个对象，后者会选择内存中已有的实例。
     * > 隐藏函数：在app中没有被使用的方法
     */
    // Java.choose("com.zkp.breath.MainActivity", {
    //     onMatch: function (instance) { //该类有多少个实例，该回调就会被触发多少次
    //         console.log("onMatch() instance: " + instance);
    //         instance.m1()//调用了隐藏函数m1()
    //     },
    //     onComplete: function () {
    //         console.log("onComplete()");
    //     }
    // });

    /**
     * 枚举所有已经加载的类
     */
    // Java.enumerateLoadedClasses({
    //     onMatch: function (_className) {
    //         console.log("[*] found instance of '" + _className + "'");
    //     },
    //     onComplete: function () {
    //         console.log("[*] class enuemration complete");
    //     }
    // });

});


function rpcExportFun() {
    Java.perform(function () {
        Java.choose("com.zkp.breath.MainActivity", {
            onMatch: function (instance) {
                console.log("onMatch() instance: " + instance);
                instance.m1()//调用了隐藏函数m1()
            },
            onComplete: function () {
                console.log("onComplete()");
            }
        });
    });
}


/**
 * Frida 的 RPC（Remote Procedure Call）功能：远程调用，以便在 Frida 脚本（这里指python文件） 中通过 RPC 调用导出的函数。
 * > 注意：根据 Frida 的要求，导出的名称不能包含大写字母或下划线
 */
rpc.exports = {
    rpc1: rpcExportFun
};