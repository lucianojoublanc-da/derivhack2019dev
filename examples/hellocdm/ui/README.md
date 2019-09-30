# DAML App Template

## Prerequisites

* [Yarn](https://yarnpkg.com/lang/en/docs/install/)

This template assumed you have a running ledger with CDM contract populated as described in the [parent folder](../).
## Quick Start

```
yarn install
```
#### 2. Run `yarn install`


#### 3. Start the sandbox and JSON API

```
daml build && daml sandbox --ledgerid myLedgerId --scenario Module:scenaro myDar.dar
```
and
```
daml json-api --ledger-host localhost --ledger-port 6865 --http-port 7575
```

#### 3. Set your ledger ID

Set the ledger id in `src/context/UserContext.js` in function `loginUser`. This should be the same value you used to start the sandbox in step 2.

#### 3. Run `yarn start`

Runs the app in the development mode.

Open http://localhost:3000 to view it in the browser. Whenever you modify any of the source files inside the `/src` folder,
the module bundler ([Webpack](http://webpack.github.io/)) will recompile the app on the fly and refresh all the connected browsers.

## Production build

Run `yarn build` to build the app for production to the build folder.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
Your app is ready to be deployed!

## License

MIT
