const { enrollMyAdmin, enrollUser } = require('./fabricNetwork');

const org1UserId = 'appUser';




async function start() {
  console.log("************Enrolling Admin*************");
  await enrollMyAdmin();
  console.log("************Enrolling User*************");
  await enrollUser(org1UserId);
}

start();
