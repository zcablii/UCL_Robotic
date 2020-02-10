
"use strict";

let DeleteCO2Source = require('./DeleteCO2Source.js')
let LoadMap = require('./LoadMap.js')
let LoadExternalMap = require('./LoadExternalMap.js')
let RegisterGui = require('./RegisterGui.js')
let DeleteRfidTag = require('./DeleteRfidTag.js')
let MoveRobot = require('./MoveRobot.js')
let DeleteThermalSource = require('./DeleteThermalSource.js')
let AddCO2Source = require('./AddCO2Source.js')
let AddThermalSource = require('./AddThermalSource.js')
let AddSoundSource = require('./AddSoundSource.js')
let DeleteSoundSource = require('./DeleteSoundSource.js')
let AddRfidTag = require('./AddRfidTag.js')

module.exports = {
  DeleteCO2Source: DeleteCO2Source,
  LoadMap: LoadMap,
  LoadExternalMap: LoadExternalMap,
  RegisterGui: RegisterGui,
  DeleteRfidTag: DeleteRfidTag,
  MoveRobot: MoveRobot,
  DeleteThermalSource: DeleteThermalSource,
  AddCO2Source: AddCO2Source,
  AddThermalSource: AddThermalSource,
  AddSoundSource: AddSoundSource,
  DeleteSoundSource: DeleteSoundSource,
  AddRfidTag: AddRfidTag,
};
