# Copyright 2025 AIT Austrian Institute of Technology GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSProfile
from rclpy.time import Duration

from rosbag2_py import convert_rclcpp_qos_to_rclpy_qos as convert_rclcpp_qos_to_rclpy_qos
from rosbag2_py import TopicMetadata

from rosbag2_py._storage import Duration as StorageDuration
from rosbag2_py._storage import QoS
from rosbag2_py._storage import rmw_qos_durability_policy_t
from rosbag2_py._storage import rmw_qos_history_policy_t
from rosbag2_py._storage import rmw_qos_liveliness_policy_t
from rosbag2_py._storage import rmw_qos_reliability_policy_t


def create_metadata(name: str,
                    type: str,  # noqa: A002
                    serialization_format: str = 'cdr',
                    id: int = 0,  # noqa: A002
                    offered_qos_profiles: list[TopicMetadata] = [],
                    type_description_hash: str = '') -> TopicMetadata:
    """Create TopicMetadata from minimal specification."""
    return TopicMetadata(id=id, name=name, type=type, serialization_format=serialization_format,
                         offered_qos_profiles=offered_qos_profiles,
                         type_description_hash=type_description_hash)


def copy_metadata(metadata: TopicMetadata, **overrides) -> TopicMetadata:
    """Create new TopicMetadata based on the old TopicMetadata with overrides."""
    kwargs = get_metadata_dict(metadata) | overrides
    return create_metadata(**kwargs)


def get_metadata_dict(metadata: TopicMetadata) -> dict[str, Any]:
    """Return metadata attributes or dict values as dict."""
    if not hasattr(metadata, '__dict__'):
        return {attr: getattr(metadata, attr) for attr in dir(metadata)
                if not attr.startswith('_') and not callable(getattr(metadata, attr))}
    else:
        return vars(metadata)


def is_any_durability_policy(metadata: TopicMetadata, policy: QoSDurabilityPolicy) -> bool:
    return any((convert_rclcpp_qos_to_rclpy_qos(qp).durability == policy
                for qp in metadata.offered_qos_profiles))


def _convert_rclpy_duration_to_rclcpp_duration(duration: Duration) -> StorageDuration:
    msg = duration.to_msg()
    return StorageDuration(seconds=msg.sec, nanoseconds=msg.nanosec)


def _convert_rclpy_qos_to_rclcpp_qos(profile: QoSProfile) -> QoS:
    c_profile = profile.get_c_qos_profile().to_dict()

    result = QoS(history_depth=profile.depth)
    result.avoid_ros_namespace_conventions(profile.avoid_ros_namespace_conventions)
    result.history(rmw_qos_history_policy_t(c_profile['history']))
    result.reliability(rmw_qos_reliability_policy_t(c_profile['reliability']))
    result.durability(rmw_qos_durability_policy_t(c_profile['durability']))
    result.lifespan(_convert_rclpy_duration_to_rclcpp_duration(profile.lifespan))
    result.deadline(_convert_rclpy_duration_to_rclcpp_duration(profile.deadline))
    result.liveliness(rmw_qos_liveliness_policy_t(c_profile['liveliness']))
    result.liveliness_lease_duration(
        _convert_rclpy_duration_to_rclcpp_duration(profile.liveliness_lease_duration))

    return result


def convert_rclpy_qos_to_rclcpp_qos(profile: list[QoSProfile] | QoSProfile) -> list[QoS]:
    # TODO (devrite): rclpy / rosbag2_py needs better conversion between QoSProfile
    #                 and rclcpp / storage QoS. Including getters too.

    if isinstance(profile, QoSProfile):
        return [_convert_rclpy_qos_to_rclcpp_qos(profile)]
    else:
        return [_convert_rclpy_qos_to_rclcpp_qos(p) for p in profile]
