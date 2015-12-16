
#include <ros/ros.h>

// MoveIt!
#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/planning_scene/planning_scene.h>

#include <moveit/kinematic_constraints/utils.h>
#include <eigen_conversions/eigen_msg.h>



int main(int argc, char **argv) {
	ros::init (argc, argv, "right_arm_kinematics");
	ros::AsyncSpinner spinner(1);
	spinner.start();
	ros::Duration(5.0);
	robot_model_loader::RobotModelLoader robotModelLoader("robot_description");
	robot_model::RobotModelPtr kinematicModel = robotModelLoader.getModel();
	planning_scene::PlanningScene planningScene(kinematicModel);

	collision_detection::CollisionRequest collisionRequest;
	collision_detection::CollisionResult collisionResult;
	planningScene.checkSelfCollision(collisionRequest, collisionResult);
	ROS_INFO_STREAM("Test 1: Current state is " << (collisionResult.collision ? "in" : "not in") << " self collision");
	robot_state::RobotState& currentState = planningScene.getCurrentStateNonConst();
	currentState.setToRandomPositions();
	collisionResult.clear();
	planningScene.checkSelfCollision(collisionRequest, collisionResult);
	ROS_INFO_STREAM("Test 2: Current state is " << (collisionResult.collision ? "in" : "not in") << " self collision");

	std::vector<double> jointValues;
	const robot_state::JointModelGroup* jointModelGroup = currentState.getJointModelGroup("arm");
	currentState.copyJointGroupPositions(jointModelGroup, jointValues);
	jointValues[0] = 1;
	currentState.setJointGroupPositions(jointModelGroup, jointValues);
	ROS_INFO_STREAM("Current state is "
					<< (currentState.satisfiesBounds(jointModelGroup) ? "valid" : "not valid"));

	collisionRequest.contacts = true;
	collisionRequest.max_contacts = 100000;
	collisionResult.clear();

	planningScene.checkSelfCollision(collisionRequest, collisionResult);
	ROS_INFO_STREAM("Test 3: Current state is " << (collisionResult.collision ? "in" : "not in") << " self collision");

	collision_detection::CollisionResult::ContactMap::const_iterator iterator;
	for(iterator = collisionResult.contacts.begin(); iterator != collisionResult.contacts.end(); ++iterator) {
		ROS_INFO("Contact between: %s and %s", iterator->first.first.c_str(), iterator->first.second.c_str());
	}

	return 0;
}
