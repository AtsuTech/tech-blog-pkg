# Set Up tailwindcss

```
npm init -y
```

```
npm install -D tailwindcss @tailwindcss/cli
```

プロジェクト直下にstatic/cssを作り、その中にinput.cssを作成し、以下の内容を追加します。
```
@import "tailwindcss";
```


```
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css --watch
```





# hilight.js set up

```
npm install highlight.js
```